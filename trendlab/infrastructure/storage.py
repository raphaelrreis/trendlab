import logging
from pathlib import Path

import pandas as pd

from trendlab.domain.models import MarketDataPoint
from trendlab.domain.ports import StorageAdapter

logger = logging.getLogger(__name__)

class ParquetStorage(StorageAdapter):
    """
    Local file system storage using Parquet format.
    """
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.raw_dir = base_dir / "data" / "raw"
        self.processed_dir = base_dir / "data" / "processed"
        
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def save_raw(self, asset: str, data: list[MarketDataPoint]) -> None:
        if not data:
            logger.warning(f"No data to save for {asset}")
            return
            
        records = [
            {
                "timestamp": d.timestamp,
                "price": d.price,
                "market_cap": d.market_cap,
                "total_volume": d.total_volume
            }
            for d in data
        ]
        df = pd.DataFrame(records)
        df.set_index("timestamp", inplace=True)
        
        path = self.raw_dir / f"{asset}.parquet"
        df.to_parquet(path)
        logger.info(f"Saved raw data for {asset} to {path}")

    def load_raw(self, asset: str) -> pd.DataFrame:
        path = self.raw_dir / f"{asset}.parquet"
        if not path.exists():
            raise FileNotFoundError(f"No raw data found for {asset}")
        return pd.read_parquet(path)

    def save_features(self, asset: str, df: pd.DataFrame) -> None:
        path = self.processed_dir / f"{asset}_features.parquet"
        df.to_parquet(path)
        logger.info(f"Saved features for {asset} to {path}")
        
    def load_features(self, asset: str) -> pd.DataFrame:
        path = self.processed_dir / f"{asset}_features.parquet"
        if not path.exists():
            raise FileNotFoundError(f"No features found for {asset}")
        return pd.read_parquet(path)
