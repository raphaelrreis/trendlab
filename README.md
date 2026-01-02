# TrendLab

**Production-Grade Crypto Market Intelligence Pipeline**

TrendLab is an end-to-end automated pipeline designed to analyze cryptocurrency market data. It handles the complete lifecycle of financial data processing—from ingestion and technical analysis to machine learning inference and reporting.

This project serves as a reference implementation for a robust, scalable, and "production-ready" quantitative research environment. It is designed for engineers and researchers who need a stable foundation to experiment with ML strategies without the overhead of building the underlying infrastructure from scratch.

---

## Project Overview

The pipeline operates in four distinct stages:

1.  **Ingestion:** resiliently fetches historical market data (Price, Volume, Market Cap) for assets like Bitcoin and Ethereum using external providers (CoinGecko).
2.  **Processing:** Computes standard technical indicators including RSI, Moving Averages (SMA 50/200), Volatility, and Drawdown metrics.
3.  **Machine Learning:** Trains predictive models (Logistic Regression) to forecast short-term market direction (Up/Down) using strictly validated time-series data.
4.  **Reporting:** Generates automated insights in Markdown and JSON formats, classifying market regimes (Trending/Ranging) and identifying risk signals.

## Key Strengths & Engineering Principles

### 1. Robust Software Engineering
*   **Clean Architecture:** The codebase follows a Hexagonal Architecture (Ports & Adapters) pattern, ensuring strict separation between domain logic, application orchestration, and infrastructure concerns.
*   **Code Quality:** Enforces high standards using `ruff` for linting, `mypy` for static type checking, and `pytest` for comprehensive unit and functional testing.
*   **CI/CD:** Fully automated GitHub Actions pipelines handle testing, linting, Docker image building, and deployment.
*   **Infrastructure as Code (IaC):** The project is cloud-agnostic and scalable, featuring Terraform scripts for AWS EKS/Azure AKS provisioning and Helm charts for Kubernetes deployment.

### 2. Data Science Rigor
*   **Prevention of Look-Ahead Bias:** A critical flaw in many financial ML projects is training on future data. TrendLab strictly enforces `TimeSeriesSplit` and careful target shifting to ensure valid out-of-sample testing.
*   **Modular Feature Engineering:** The system is designed to allow new technical indicators or external data sources to be plugged in without refactoring the core pipeline.

### 3. Scalability & Cloud Readiness
*   **Containerization:** Fully Dockerized application ensuring consistency across development, testing, and production environments.
*   **Orchestration:** Ready for horizontal scaling via Kubernetes, allowing parallel processing of multiple assets.

---

## Roadmap & Future Improvements

We have identified several areas for future development to evolve TrendLab from a solid framework into a high-performance trading engine:

*   **Advanced ML Models:** Transition from baseline Logistic Regression to non-linear models like XGBoost, LSTMs, or Transformers to capture complex market dynamics.
*   **Alternative Data:** Integrate on-chain metrics, social sentiment analysis, and macroeconomic indicators to improve predictive signal-to-noise ratio.
*   **Enterprise Data Layer:** Replace local Parquet persistence with a scalable solution using S3-compatible object storage and a time-series database (e.g., TimescaleDB) to handle terabytes of tick-level data.
*   **Backtesting Engine:** Implement a full event-driven backtester to simulate PnL, slippage, and fees, providing a realistic assessment of strategy profitability beyond simple directional accuracy.
*   **API Scaling:** Implement an internal caching proxy or upgrade data providers to handle high-frequency requests without hitting rate limits.

---

## Technical Setup

### Prerequisites
*   Python 3.9+
*   Docker & Docker Compose
*   Poetry (for dependency management)

### Quickstart (Local via Docker)

The easiest way to run the full service locally:

```bash
make build
make up
```

The API will be available at `http://localhost:8080`.

Trigger a pipeline run:
```bash
make run-local
```

Check logs:
```bash
docker-compose logs -f
```

### Manual Development Setup

```bash
make setup
# Run the pipeline for Bitcoin and Ethereum
poetry run trendlab run --assets btc --assets eth --days 365
```

## Infrastructure & Deployment

*   **Kubernetes:** Helm charts for Dev, Hml, and Prd environments are located in `deploy/helm`.
*   **Terraform:** Infrastructure definitions for AWS and Azure are available in `infra/`.
*   **CI/CD:** Workflows defined in `.github/workflows`.

## License

MIT