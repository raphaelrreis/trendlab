import logging
from datetime import datetime
from pathlib import Path
from typing import cast, Any

from trendlab.domain.models import Asset, Prediction, MarketInsight
from trendlab.domain.ports import DataProvider, StorageAdapter
from trendlab.infrastructure.coingecko import CoinGeckoProvider
from trendlab.infrastructure.storage import ParquetStorage
from trendlab.analytics.features import FeatureEngineer
from trendlab.analytics.engine import ModelEngine
from trendlab.analytics.reporting import ReportGenerator

logger = logging.getLogger(__name__)

class PipelineService:
    def __init__(self, root_dir: Path):
        self.provider: DataProvider = CoinGeckoProvider()
        self.storage: StorageAdapter = ParquetStorage(root_dir)
        self.engineer = FeatureEngineer()
        self.reporter = ReportGenerator(root_dir / "reports")

    def fetch_data(self, assets: list[Asset], days: int):
        for asset in assets:
            data = self.provider.fetch_history(asset, days)
            self.storage.save_raw(asset.symbol, data)

    def build_features(self, assets: list[Asset]):
        for asset in assets:
            try:
                raw_df = self.storage.load_raw(asset.symbol)
                features_df = self.engineer.compute_features(raw_df)
                self.storage.save_features(asset.symbol, features_df)
            except Exception as e:
                logger.error(f"Failed to build features for {asset.name}: {e}")

    def run_inference(self, assets: list[Asset], model_type: str = "logistic") -> list[Prediction]:
        predictions = []
        for asset in assets:
            try:
                df = self.storage.load_features(asset.symbol)
                dataset = self.engineer.create_dataset(df)
                
                if dataset.empty:
                    logger.warning(f"Insufficient data for {asset.name}")
                    continue
                
                # Split features and target
                # 'target_next_day_up' is at index t, representing t+1 outcome
                X = dataset.drop(columns=['target_next_day_up'])
                y = dataset['target_next_day_up']
                
                # Train
                model = ModelEngine(model_type=model_type)
                metrics = model.train(X, y)
                
                # Inference on latest data (the last row of df, which might have been dropped in create_dataset if target was nan)  # noqa: E501
                # We need the most recent row from df (which represents "today") to predict "tomorrow"
                latest_row = df.iloc[[-1]].drop(columns=['target_next_day_up'], errors='ignore')
                
                # Check if latest row has NaNs (e.g. not enough history for rolling window)
                if latest_row.isna().any().any():
                     logger.warning(f"Cannot predict for {asset.name}: latest data incomplete.")
                     continue

                # Force cast to float for mypy satisfaction
                prob_raw = model.predict_proba(latest_row).iloc[0, 1]
                prob_up = float(cast(float, prob_raw))
                
                # Heuristic signal generation
                signal = "NEUTRAL"
                if prob_up > 0.55:
                    signal = "BULLISH"
                elif prob_up < 0.45:
                    signal = "BEARISH"
                    
                confidence = (abs(prob_up - 0.5) * 2)  # Scale 0.5-1.0 to 0-1
                
                predictions.append(Prediction(
                    asset=asset.symbol,
                    date=datetime.now(),
                    model_name=model_type,
                    horizon_days=1,
                    probability_up=prob_up,
                    signal=signal,
                    confidence_score=confidence,
                    supporting_metrics=metrics
                ))
                
            except Exception as e:
                logger.error(f"Inference failed for {asset.name}: {e}")
                
        return predictions

    def generate_insights(self, assets: list[Asset]) -> list[MarketInsight]:
        insights = []
        for asset in assets:
            try:
                df = self.storage.load_features(asset.symbol)
                latest = df.iloc[-1]
                
                # Simple heuristics
                # Use float() to ensure python types for comparison
                sma_50 = float(latest['sma_50'])
                sma_200 = float(latest['sma_200'])
                trend = "UP" if sma_50 > sma_200 else "DOWN"
                
                vol_30d = float(latest['vol_30d'])
                vol_state = "HIGH" if vol_30d > 0.05 else "LOW" # 5% daily vol threshold
                
                rsi_14 = float(latest['rsi_14'])
                regime = "TRENDING" if abs(rsi_14 - 50) > 10 else "RANGING"
                
                price = float(latest['price'])
                drawdown = float(latest['drawdown'])
                
                summary = (
                    f"Price ${price:.2f}. "
                    f"Volatility is {vol_state} ({vol_30d:.1%}). "
                    f"RSI at {rsi_14:.1f} suggests {regime.lower()} behavior."
                )
                
                insights.append(MarketInsight(
                    asset=asset.symbol,
                    date=datetime.now(),
                    trend=trend,
                    volatility_state=vol_state,
                    regime=regime,
                    drawdown_pct=drawdown,
                    summary=summary
                ))
            except Exception as e:
                logger.error(f" Insight generation failed for {asset.name}: {e}")
        return insights

    def run_full_pipeline(self, assets: list[Asset], days: int):
        logger.info("--- Starting Pipeline ---")
        self.fetch_data(assets, days)
        self.build_features(assets)
        preds = self.run_inference(assets)
        insights = self.generate_insights(assets)
        
        md_path = self.reporter.generate_markdown(insights, preds)
        self.reporter.generate_json(insights, preds)
        
        logger.info(f"Report generated: {md_path}")
        logger.info("--- Pipeline Complete ---")
