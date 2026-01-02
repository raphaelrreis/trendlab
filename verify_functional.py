import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import shutil

# Add current directory to sys.path to ensure imports work
sys.path.append(str(Path.cwd()))

from trendlab.domain.models import Asset, MarketDataPoint, MarketInsight
from trendlab.infrastructure.storage import ParquetStorage
from trendlab.analytics.features import FeatureEngineer
from trendlab.analytics.engine import ModelEngine

def test_domain():
    print("✅ Testing Domain Layer...")
    btc = Asset(symbol="btc", name="Bitcoin", provider_id="bitcoin")
    assert btc.symbol == "btc"
    
    dp = MarketDataPoint(
        timestamp=datetime.now(),
        price=50000.0,
        market_cap=1e12,
        total_volume=1e9
    )
    assert dp.price == 50000.0
    print("   -> Domain models OK")

def test_infrastructure():
    print("\n✅ Testing Infrastructure Layer (Storage)...")
    # Setup temp dir
    tmp_dir = Path("temp_test_data")
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    
    storage = ParquetStorage(tmp_dir)
    
    # Create dummy data
    data = [
        MarketDataPoint(datetime.now() - timedelta(days=i), 100.0 + i, 1000.0, 100.0)
        for i in range(5)
    ]
    
    # Test Save/Load Raw
    storage.save_raw("test_asset", data)
    df_raw = storage.load_raw("test_asset")
    assert not df_raw.empty
    assert len(df_raw) == 5
    print("   -> Storage save/load raw OK")
    
    # Cleanup
    shutil.rmtree(tmp_dir)

def test_analytics():
    print("\n✅ Testing Analytics Layer...")
    
    # 1. Features
    dates = pd.date_range(start="2023-01-01", periods=300) # Enough for 200 SMA
    df = pd.DataFrame({
        "price": np.linspace(100, 200, 300) + np.random.normal(0, 2, 300),
        "total_volume": np.random.randint(1000, 5000, 300),
        "market_cap": np.linspace(10000, 20000, 300)
    }, index=dates)
    
    engineer = FeatureEngineer()
    df_features = engineer.compute_features(df)
    
    assert "rsi_14" in df_features.columns
    assert "sma_200" in df_features.columns
    assert "target_next_day_up" in df_features.columns
    print("   -> Feature Engineering OK")
    
    # 2. Model
    dataset = engineer.create_dataset(df_features)
    X = dataset.drop(columns=['target_next_day_up'])
    y = dataset['target_next_day_up']
    
    model = ModelEngine(model_type="logistic")
    metrics = model.train(X, y)
    
    assert "accuracy" in metrics
    assert "auc" in metrics
    
    # Predict
    last_row = df_features.iloc[[-1]].drop(columns=['target_next_day_up'], errors='ignore')
    prob = model.predict_proba(last_row).iloc[0, 1]
    print(f"   -> Model Training & Prediction OK (Prob: {prob:.2f})")

if __name__ == "__main__":
    print("🚀 Starting Functional Verification for TrendLab\n")
    try:
        test_domain()
        test_infrastructure()
        test_analytics()
        print("\n🎉 ALL FUNCTIONAL TESTS PASSED!")
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
