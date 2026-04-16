"""Ingestion worker — standalone process that runs the pipeline.

Usage:
    # One-shot run:
    python -m workers.ingest

    # Continuous loop (every N minutes):
    python -m workers.ingest --loop --interval 30
"""
from __future__ import annotations

import argparse
import asyncio
import sys
from datetime import datetime, timezone

# Ensure the backend package is importable
sys.path.insert(0, ".")

from app.db.session import SessionLocal
from app.modules.ingestion.pipeline import run_pipeline


async def run_once() -> None:
    print(f"[{datetime.now(timezone.utc).isoformat()}] Starting ingestion run...")
    async with SessionLocal() as session:
        stats = await run_pipeline(session)
    print(f"[{datetime.now(timezone.utc).isoformat()}] Done: {stats}")


async def run_loop(interval_minutes: int) -> None:
    while True:
        try:
            await run_once()
        except Exception as exc:
            print(f"[ingestion] error: {exc}")
        print(f"[ingestion] sleeping {interval_minutes} min...")
        await asyncio.sleep(interval_minutes * 60)


def main() -> None:
    parser = argparse.ArgumentParser(description="HotPulse ingestion worker")
    parser.add_argument("--loop", action="store_true", help="Run continuously")
    parser.add_argument("--interval", type=int, default=30, help="Minutes between runs")
    args = parser.parse_args()

    if args.loop:
        asyncio.run(run_loop(args.interval))
    else:
        asyncio.run(run_once())


if __name__ == "__main__":
    main()
