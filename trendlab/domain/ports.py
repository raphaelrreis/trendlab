from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Protocol, Dict, Any
import pandas as pd

from trendlab.domain.models import Asset, MarketDataPoint

class DataProvider(Protocol):
    """Interface for fetching market data."""
    
    def fetch_history(self, asset: Asset, days: int) -> List[MarketDataPoint]:
        ...

class StorageAdapter(Protocol):
    """Interface for persisting data."""
    
    def save_raw(self, asset: str, data: List[MarketDataPoint]) -> None:
        ...
        
    def load_raw(self, asset: str) -> pd.DataFrame:
        ...

    def save_features(self, asset: str, df: pd.DataFrame) -> None:
        ...
        
    def load_features(self, asset: str) -> pd.DataFrame:
        ...

class MLModel(ABC):
    """Abstract base class for ML models."""
    
    @abstractmethod
    def train(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """Train and return evaluation metrics."""
        ...

    @abstractmethod
    def predict(self, X: pd.DataFrame) -> pd.Series:
        ...
    
    @abstractmethod
    def predict_proba(self, X: pd.DataFrame) -> pd.DataFrame:
        ...
