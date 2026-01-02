import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class FeatureEngineer:
    """
    Computes technical indicators and market metrics.
    Ensures strict adherence to preventing look-ahead bias.
    """

    def compute_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Enriches the dataframe with technical indicators.
        Input dataframe must be indexed by timestamp.
        """
        data = df.copy().sort_index()
        
        # 1. Returns
        data['log_ret'] = np.log(data['price'] / data['price'].shift(1))
        
        # 2. Volatility (Rolling)
        data['vol_7d'] = data['log_ret'].rolling(window=7).std()
        data['vol_30d'] = data['log_ret'].rolling(window=30).std()
        
        # 3. Momentum (RSI)
        data['rsi_14'] = self._calculate_rsi(data['price'], 14)
        
        # 4. Trend (SMA Crossovers)
        data['sma_50'] = data['price'].rolling(window=50).mean()
        data['sma_200'] = data['price'].rolling(window=200).mean()
        data['trend_signal'] = (data['sma_50'] > data['sma_200']).astype(int)
        
        # 5. Drawdown
        rolling_max = data['price'].rolling(window=365, min_periods=1).max()
        data['drawdown'] = (data['price'] / rolling_max) - 1
        
        # 6. Volume Change
        data['vol_change_5d'] = data['total_volume'].pct_change(periods=5)
        
        # 7. Target (Next day direction) - SHIFTED BACKWARDS
        # Target: 1 if Price(t+1) > Price(t), else 0
        # We shift(-1) so that row T contains the outcome at T+1
        # Use float to allow NaN for the last row
        data['target_next_day_up'] = (data['price'].shift(-1) > data['price']).astype(float)
        data.loc[data['price'].shift(-1).isna(), 'target_next_day_up'] = np.nan
        
        return data

    def _calculate_rsi(self, series: pd.Series, period: int = 14) -> pd.Series:
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def create_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepares the final dataset for training.
        Removes rows with NaN features or targets.
        """
        # Drop rows where we don't have enough history for features
        # AND drop the last row because it has no target (for training)
        return df.dropna()
