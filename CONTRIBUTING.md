# Contributing to TrendLab

We welcome contributions from engineers who care about code quality and rigor.

## Development Workflow

1.  **Setup Environment**:
    ```bash
    make setup
    ```

2.  **Coding Standards**:
    - We use `ruff` for linting and formatting.
    - We use `mypy` for strict type checking.
    - Run `make lint` before committing.

3.  **Testing**:
    - Add unit tests for new logic in `tests/`.
    - Run `make test` to ensure no regressions.

## Pull Request Guidelines

- **Atomic Commits**: Keep changes focused.
- **Type Hints**: All functions must have type hints.
- **No Magic Numbers**: Use constants or config.
- **Leakage Check**: If modifying features, verify you are not using future data to predict the past.

## Adding a New Data Provider

1.  Implement the `DataProvider` protocol in `trendlab/infrastructure/`.
2.  Update `PipelineService` or use a factory to inject the new provider.
