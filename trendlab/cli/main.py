import typer
import logging
from pathlib import Path
from typing import List, Optional

from trendlab.application.pipeline import PipelineService
from trendlab.domain.models import Asset
from trendlab.utils.logging import setup_logging

app = typer.Typer(
    name="trendlab",
    help="Crypto Market Intelligence & Prediction Pipeline",
    add_completion=False
)

# Common assets map
ASSET_MAP = {
    "btc": Asset("btc", "Bitcoin", "bitcoin"),
    "eth": Asset("eth", "Ethereum", "ethereum"),
    "sol": Asset("sol", "Solana", "solana"),
    "ada": Asset("ada", "Cardano", "cardano"),
    "dot": Asset("dot", "Polkadot", "polkadot")
}

def get_service() -> PipelineService:
    root = Path.cwd()
    return PipelineService(root)

@app.callback()
def main(verbose: bool = False):
    """
    TrendLab: Production-grade ML pipeline for crypto insights.
    """
    level = logging.DEBUG if verbose else logging.INFO
    setup_logging(level)

@app.command()
def fetch(
    assets: List[str] = typer.Option(["btc", "eth"], help="List of asset symbols (btc, eth, sol)"),
    days: int = typer.Option(365, help="Days of history to fetch")
):
    """Fetch historical market data from CoinGecko."""
    service = get_service()
    target_assets = [ASSET_MAP[a.lower()] for a in assets if a.lower() in ASSET_MAP]
    
    if not target_assets:
        typer.echo("No valid assets selected.")
        raise typer.Exit(code=1)
        
    service.fetch_data(target_assets, days)
    typer.echo(f"Fetched data for: {', '.join(a.symbol for a in target_assets)}")

@app.command()
def build_features(
    assets: List[str] = typer.Option(["btc", "eth"], help="List of asset symbols")
):
    """Compute technical indicators and features."""
    service = get_service()
    target_assets = [ASSET_MAP[a.lower()] for a in assets if a.lower() in ASSET_MAP]
    service.build_features(target_assets)
    typer.echo("Feature engineering complete.")

@app.command()
def train(
    assets: List[str] = typer.Option(["btc", "eth"], help="List of asset symbols"),
    model: str = typer.Option("logistic", help="Model type: logistic, boosting")
):
    """Train models and output predictions."""
    service = get_service()
    target_assets = [ASSET_MAP[a.lower()] for a in assets if a.lower() in ASSET_MAP]
    preds = service.run_inference(target_assets, model)
    
    for p in preds:
        typer.echo(f"{p.asset.upper()}: {p.signal} ({p.probability_up:.1%} prob) - Conf: {p.confidence_score:.2f}")

@app.command()
def run(
    assets: List[str] = typer.Option(["btc", "eth"], help="List of asset symbols"),
    days: int = typer.Option(365, help="Days of history to fetch")
):
    """Run the full pipeline end-to-end."""
    service = get_service()
    target_assets = [ASSET_MAP[a.lower()] for a in assets if a.lower() in ASSET_MAP]
    service.run_full_pipeline(target_assets, days)

if __name__ == "__main__":
    app()
