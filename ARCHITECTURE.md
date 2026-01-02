# Architecture Design Document

## System Overview

TrendLab is designed as a modular, layered monolith. It strictly follows separation of concerns to ensure maintainability and testability.

### Layers

1.  **Domain (`trendlab/domain`)**
    - Contains pure Python data classes (`Asset`, `Prediction`) and interfaces (`Protocol`).
    - **Rule**: No dependencies on external frameworks (pandas is allowed for data structures).

2.  **Infrastructure (`trendlab/infrastructure`)**
    - Implements Domain interfaces.
    - `CoinGeckoProvider`: Handles HTTP requests, retries, and rate limits.
    - `ParquetStorage`: Manages local file system persistence using performant Parquet files.

3.  **Analytics (`trendlab/analytics`)**
    - Core business logic for data science.
    - `FeatureEngineer`: Stateless transformation of raw price data into feature sets.
    - `ModelEngine`: Wraps scikit-learn to provide a simplified training/inference API ensuring time-series safety.

4.  **Application (`trendlab/application`)**
    - `PipelineService`: Orchestrates the flow: Fetch -> Store -> Transform -> Train -> Report.
    - Acts as the entry point for the CLI.

5.  **CLI (`trendlab/cli`)**
    - Uses `typer` to expose Application services to the user.
    - Handles arguments, parsing, and console output.

## Data Flow

1.  **Ingestion**: `fetch` command triggers `CoinGeckoProvider`. Data is normalized to UTC and saved as raw Parquet.
2.  **Processing**: `build-features` loads raw data, applies `FeatureEngineer`, and saves `*_features.parquet`.
3.  **Learning**: `train` loads feature sets.
    - Rows with `NaN` (due to lags/windows) are dropped.
    - `TimeSeriesSplit` creates 5 folds for validation.
    - Model is refit on *all* available history for the final inference.
4.  **Inference**: The model predicts the probability of an "Up" move for $t+1$ based on features at $t$ (today).

## Design Decisions

- **Local Storage**: We use a simple "Data Lake" directory structure (`data/raw`, `data/processed`) instead of a database for simplicity and portability. Parquet is chosen for type preservation and speed.
- **Scikit-Learn**: Chosen over PyTorch/TensorFlow because tabular financial data often performs best with simple linear or tree-based models, and complexity adds risk of overfitting.
- **Typer**: Chosen for its developer experience and type-hint integration.
