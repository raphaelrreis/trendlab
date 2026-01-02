from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class AssetClass(str, Enum):
    CRYPTO = "crypto"
    EQUITY = "equity"
    FOREX = "forex"

@dataclass(frozen=True)
class Asset:
    symbol: str  # e.g., "btc"
    name: str    # e.g., "bitcoin"
    provider_id: str  # e.g., "bitcoin" for CoinGecko

@dataclass
class MarketDataPoint:
    timestamp: datetime
    price: float
    market_cap: float
    total_volume: float

@dataclass
class Prediction:
    asset: str
    date: datetime
    model_name: str
    horizon_days: int
    probability_up: float
    signal: str  # "BULLISH", "BEARISH", "NEUTRAL"
    confidence_score: float
    supporting_metrics: dict[str, float]

@dataclass
class MarketInsight:
    asset: str
    date: datetime
    trend: str
    volatility_state: str
    regime: str
    drawdown_pct: float
    summary: str
