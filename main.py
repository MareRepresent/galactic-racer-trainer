"""CLI entry point for galactic-racer-trainer."""
from __future__ import annotations

import argparse
import time
from pathlib import Path

from galactic_racer_trainer.bootstrap import TrainerBootstrap
from galactic_racer_trainer.utils.logger import setup_logging


def main() -> int:
    parser = argparse.ArgumentParser(prog="galactic-racer-trainer")
    parser.add_argument("--config", type=Path, default=Path("config/trainer.toml"))
    parser.add_argument("--log-dir", type=Path, default=Path("logs"))
    args = parser.parse_args()

    setup_logging(log_dir=args.log_dir)
    boot = TrainerBootstrap(config_path=args.config)
    boot.start()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        boot.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())