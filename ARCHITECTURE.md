# Architecture & Technology Stack

TrendLab is designed with a focus on maintainability, scalability, and strict adherence to software engineering best practices. This document outlines the core technologies and architectural patterns used in the system.

## Architectural Pattern: Hexagonal (Ports & Adapters)

The application is structured to decouple the core business logic from external dependencies.

*   **Domain Layer (`trendlab/domain`):** Contains pure Python dataclasses and interfaces (Ports). No external dependencies. Defines *what* the system does (e.g., `Asset`, `Prediction`).
*   **Application Layer (`trendlab/application`):** Orchestrates data flows and use cases (e.g., `PipelineService`). Implements the business rules.
*   **Infrastructure Layer (`trendlab/infrastructure`):** Implements the interfaces defined in the Domain (Adapters). Handles IO, such as API calls (`CoinGeckoProvider`) and file storage (`ParquetStorage`).
*   **Analytics Layer (`trendlab/analytics`):** specialized logic for Feature Engineering and Model Training, encapsulating the Data Science complexity.

## Technology Stack

### Core Application
*   **Language:** Python 3.9+ (chosen for its rich Data Science ecosystem).
*   **Dependency Management:** [Poetry](https://python-poetry.org/) - Ensures deterministic builds and dependency resolution.
*   **CLI Framework:** [Typer](https://typer.tiangolo.com/) - Provides an intuitive command-line interface.
*   **API Framework:** [FastAPI](https://fastapi.tiangolo.com/) - High-performance, async-ready web framework for serving predictions.

### Data Science & Machine Learning
*   **Data Processing:** [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/).
*   **Machine Learning:** [Scikit-learn](https://scikit-learn.org/) - Used for pipeline construction, preprocessing, and model training.
*   **Validation:** [TimeSeriesSplit](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html) - Strictly enforced to prevent look-ahead bias in financial data.

### Code Quality & Standards
*   **Linting:** [Ruff](https://docs.astral.sh/ruff/) - Extremely fast Python linter, replacing Flake8/Isort.
*   **Type Checking:** [Mypy](https://mypy-lang.org/) - Enforces static typing to catch errors at build time.
*   **Testing:** [Pytest](https://docs.pytest.org/) - Comprehensive test suite with coverage reporting.

### Infrastructure & DevOps
*   **Containerization:** Docker & Docker Compose - Ensures consistent runtime environments.
*   **Orchestration:** Kubernetes (K8s) - The target deployment platform for scalability.
*   **Package Management:** Helm - Manages Kubernetes manifests across environments (Dev, Hml, Prd).
*   **Infrastructure as Code:** Terraform - Provisioning scripts for AWS EKS and Azure AKS.
*   **CI/CD:** GitHub Actions - Automates the pipeline for Linting, Testing, Building, and Deploying.

## Data Flow

1.  **Trigger:** User initiates run via CLI or API.
2.  **Fetch:** `CoinGeckoProvider` requests market data (handles rate limits/retries).
3.  **Store Raw:** Raw JSON data is normalized and stored as Parquet files.
4.  **Feature Engineering:** Technical indicators are computed vectorized via Pandas.
5.  **Training/Inference:**
    *   *Training:* Data is split chronologically. Model is trained on past, validated on "future".
    *   *Inference:* Model predicts the probability of an "Up" move for the next interval based on the latest available data.
6.  **Report:** Results are aggregated into Markdown reports and JSON artifacts for consumption.