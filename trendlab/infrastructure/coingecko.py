import time
import logging
from datetime import datetime, timezone
from typing import List, Any, Dict

import requests
from requests.adapters import HTTPAdapter, Retry

from trendlab.domain.models import Asset, MarketDataPoint
from trendlab.domain.ports import DataProvider

logger = logging.getLogger(__name__)

class CoinGeckoProvider(DataProvider):
    """
    CoinGecko API Client implementation.
    Uses public endpoints with strict rate limiting handling.
    """
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))
        return session

    def fetch_history(self, asset: Asset, days: int) -> List[MarketDataPoint]:
        """
        Fetches historical market data (price, market cap, volume).
        
        Args:
            asset: Asset entity containing provider_id (e.g. 'bitcoin')
            days: Number of days of history
        """
        endpoint = f"{self.BASE_URL}/coins/{asset.provider_id}/market_chart"
        params = {
            "vs_currency": "usd",
            "days": days,
            "interval": "daily"
        }
        
        try:
            logger.info(f"Fetching {days} days of data for {asset.name}...")
            response = self.session.get(endpoint, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            return self._parse_response(data)
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                logger.error("Rate limit hit. Waiting 60s...")
                time.sleep(60)
                # Simple recursive retry once for demo purposes, 
                # in prod use a decorator or robust poller
                return self.fetch_history(asset, days)
            logger.error(f"HTTP Error fetching data for {asset.name}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching data for {asset.name}: {e}")
            raise

    def _parse_response(self, data: Dict[str, Any]) -> List[MarketDataPoint]:
        prices = data.get("prices", [])
        market_caps = data.get("market_caps", [])
        total_volumes = data.get("total_volumes", [])
        
        points = []
        # CoinGecko returns [timestamp_ms, value]
        # We assume lengths match. In prod, align strictly by timestamp.
        for i in range(len(prices)):
            ts_ms = prices[i][0]
            dt = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)
            
            point = MarketDataPoint(
                timestamp=dt,
                price=float(prices[i][1]),
                market_cap=float(market_caps[i][1]) if i < len(market_caps) else 0.0,
                total_volume=float(total_volumes[i][1]) if i < len(total_volumes) else 0.0
            )
            points.append(point)
            
        return points
