import numpy as np
import pandas as pd
import pytest

from trendlab.analytics.features import FeatureEngineer


@pytest.fixture
def sample_data():
    dates = pd.date_range(start="2023-01-01", periods=100)
    df = pd.DataFrame({
        "price": np.linspace(100, 200, 100) + np.random.normal(0, 5, 100),
        "total_volume": np.random.randint(1000, 5000, 100),
        "market_cap": np.linspace(10000, 20000, 100)
    }, index=dates)
    return df

def test_feature_engineering_creates_columns(sample_data):
    engineer = FeatureEngineer()
    features = engineer.compute_features(sample_data)
    
    expected_cols = ["log_ret", "vol_7d", "rsi_14", "sma_50", "target_next_day_up"]
    for col in expected_cols:
        assert col in features.columns

def test_no_leakage_in_target(sample_data):
    engineer = FeatureEngineer()
    df = engineer.compute_features(sample_data)
    
    # Check manual calculation of target
    # If price goes up tomorrow, today's target should be 1
    
    # Pick a random index t (not the last one)
    idx = 50
    current_price = df.iloc[idx]['price']
    next_price = df.iloc[idx + 1]['price']
    
    target = df.iloc[idx]['target_next_day_up']
    
    expected_target = 1 if next_price > current_price else 0
    assert target == expected_target

def test_create_dataset_drops_nans(sample_data):
    engineer = FeatureEngineer()
    df = engineer.compute_features(sample_data)
    clean_df = engineer.create_dataset(df)
    
    assert not clean_df.isnull().values.any()
