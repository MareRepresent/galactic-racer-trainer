"""Helper that prints current pointer-chain addresses for a running game."""
from __future__ import annotations

import argparse
from pathlib import Path

from galactic_racer_trainer.config.loader import load_config
from galactic_racer_trainer.drivers.process_scanner import ProcessScanner
from galactic_racer_trainer.utils.logger import setup_logging


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("config/trainer.toml"))
    args = parser.parse_args()
    setup_logging()

    cfg = load_config(args.config)
    scanner = ProcessScanner(cfg.target_process)
    if not scanner.attach():
        print("game not running")
        return 1

    for name, base in cfg.pointers.items():
        chain = cfg.offsets.get(f"{name}_chain", [0x0])
        try:
            addr = scanner.resolve(base, chain)
            print(f"{name:16s} -> 0x{addr:X}  chain={chain}")
        except Exception as exc:  # noqa: BLE001
            print(f"{name:16s} -> FAILED ({exc})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())