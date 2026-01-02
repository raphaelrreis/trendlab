# TrendLab 🚀

> **Production-grade Crypto Market Intelligence Pipeline**

TrendLab is a robust Python-based ML pipeline that fetches historical crypto market data, computes technical indicators, and trains time-series validated machine learning models to generate short-term directional probabilities and actionable market insights.

**⚠️ DISCLAIMER: This software is for educational and research purposes only. It is NOT financial advice.**

## Features

- **Automated Data Ingestion**: Resilient fetching from CoinGecko.
- **Time-Series Rigor**: Strict prevention of look-ahead bias using `TimeSeriesSplit`.
- **ML Engine**: Scikit-learn pipelines with Logistic Regression.
- **Insight Generation**: Produces "Decision Insight" reports (Markdown/JSON).
- **Platform Ready**: Dockerized, Kubernetes-ready (Helm), and Infrastructure-as-Code (Terraform).

## Quickstart (Local)

### Docker Compose

The easiest way to run the full service locally:

```bash
make build
make up
```

The API will be available at `http://localhost:8080`.

Trigger a run:
```bash
make run-local
```

Check logs:
```bash
docker-compose logs -f
```

### Manual Python Setup

```bash
make setup
poetry run trendlab run --assets btc --assets eth --days 365
```

## Infrastructure & Deployment

### Kubernetes (Helm)

We use Helm to deploy to Dev, Hml, and Prd environments.
See [deploy/README.md](deploy/README.md) for details.

### Infrastructure (Terraform)

We support both AWS EKS and Azure AKS.
See [infra/README.md](infra/README.md) for provisioning instructions.

### CI/CD

GitHub Actions pipelines are defined in `.github/workflows/`:
- `ci.yml`: Runs on PRs (Lint, Test, Build).
- `deploy.yml`: Pushes to GHCR and deploys to K8s via Helm (requires `KUBE_CONFIG` secret).

## API Usage

**POST /run**
```json
{
  "assets": ["btc", "eth", "sol"],
  "days": 365,
  "horizon": 1
}
```

**GET /health**
Returns 200 OK if service is healthy.

## Methodology

### Feature Engineering
We compute a standard set of technical factors including:
- **Momentum**: RSI (14-day), Price ROC.
- **Volatility**: 7-day and 30-day rolling log return std dev.
- **Trend**: SMA 50/200 crossovers.
- **Regime**: Market state classification (Trending vs Ranging).

### Model Evaluation
To avoid "leakage" common in financial ML:
- Targets are shifted: $y_t = \mathbb{I}(Price_{t+1} > Price_t)$.
- Validation uses **Walk-Forward** (expanding window) splitting.

## License

MIT
