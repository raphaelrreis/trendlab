import logging
import os
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel

from trendlab.application.pipeline import PipelineService
from trendlab.domain.models import Asset
from trendlab.utils.logging import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger("trendlab.api")

app = FastAPI(
    title="TrendLab API",
    description="Crypto Market Intelligence Pipeline API",
    version="0.1.0"
)

# Configuration from Env
# Default to local data/reports if /app doesn't exist (local dev)
if Path("/app").exists() and os.access("/app", os.W_OK):
    DEFAULT_DATA_DIR = "/app/data"
    DEFAULT_REPORT_DIR = "/app/reports"
else:
    DEFAULT_DATA_DIR = "data"
    DEFAULT_REPORT_DIR = "reports"

DATA_DIR = Path(os.getenv("DATA_DIR", DEFAULT_DATA_DIR))
REPORT_DIR = Path(os.getenv("REPORT_DIR", DEFAULT_REPORT_DIR))

# Ensure persistence dirs exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Common assets map (shared with CLI, ideally moved to config)
ASSET_MAP = {
    "btc": Asset("btc", "Bitcoin", "bitcoin"),
    "eth": Asset("eth", "Ethereum", "ethereum"),
    "sol": Asset("sol", "Solana", "solana"),
    "ada": Asset("ada", "Cardano", "cardano"),
    "dot": Asset("dot", "Polkadot", "polkadot")
}

class RunRequest(BaseModel):
    assets: list[str] = ["btc", "eth"]
    days: int = 365
    horizon: int = 1

def run_pipeline_task(req: RunRequest):
    """Background task to run the pipeline."""
    try:
        logger.info(f"Starting background pipeline run for {req.assets}")
        # Initialize service with persistence paths
        # Note: PipelineService currently takes root_dir and appends /data and /reports
        # We need to hack it slightly or refactor PipelineService to accept specific dirs.
        # For minimal changes, we pass the parent of DATA_DIR if the structure matches,
        # or we update PipelineService. 
        # Let's assume PipelineService uses root / "data" / "raw" etc.
        # We will point it to /app.
        
        service_root = Path("/app") if Path("/app").exists() else Path.cwd()
        service = PipelineService(service_root)
        
        target_assets = []
        for a in req.assets:
            if a.lower() in ASSET_MAP:
                target_assets.append(ASSET_MAP[a.lower()])
            else:
                logger.warning(f"Skipping unknown asset: {a}")
        
        if not target_assets:
            logger.error("No valid assets to process.")
            return

        service.run_full_pipeline(target_assets, req.days)
        logger.info("Background pipeline run completed successfully.")
        
    except Exception as e:
        logger.error(f"Pipeline run failed: {e}", exc_info=True)

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "0.1.0"}

@app.post("/run")
def trigger_run(req: RunRequest, background_tasks: BackgroundTasks):
    """Triggers an asynchronous pipeline run."""
    background_tasks.add_task(run_pipeline_task, req)
    return {
        "message": "Pipeline run triggered",
        "config": req.dict(),
        "status": "processing"
    }

# Liveness probe helper
@app.get("/live")
def liveness():
    return {"status": "alive"}
