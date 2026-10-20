"""Entry bootstrap: wires config, memory driver, overlay and feature modules."""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

from galactic_racer_trainer.config.loader import load_config
from galactic_racer_trainer.drivers.process_scanner import ProcessScanner
from galactic_racer_trainer.drivers.memory_writer import MemoryWriter
from galactic_racer_trainer.overlay_core.overlay import OverlayWindow
from galactic_racer_trainer.feature_hub.registry import FeatureRegistry

log = logging.getLogger("grt.bootstrap")


@dataclass
class TrainerBootstrap:
    config_path: Path = field(default_factory=lambda: Path("config/trainer.toml"))
    overlay: OverlayWindow | None = None
    registry: FeatureRegistry | None = None

    def start(self) -> None:
        cfg = load_config(self.config_path)
        log.info("loaded config: %s (process=%s)", cfg.profile, cfg.target_process)

        scanner = ProcessScanner(cfg.target_process)
        if not scanner.attach():
            raise RuntimeError(f"target process not found: {cfg.target_process}")

        writer = MemoryWriter(scanner.handle)
        self.overlay = OverlayWindow(cfg.overlay)
        self.overlay.spawn()

        self.registry = FeatureRegistry(cfg, scanner, writer, self.overlay)
        self.registry.enable_all(cfg.enabled_features)
        log.info("trainer ready — %d features active", self.registry.active_count)

    def stop(self) -> None:
        if self.registry:
            self.registry.disable_all()
        if self.overlay:
            self.overlay.close()