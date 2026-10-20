"""Feature registry — every cheat module registers itself here."""
from __future__ import annotations

import logging
from typing import Callable

from galactic_racer_trainer.config.loader import TrainerConfig
from galactic_racer_trainer.drivers.process_scanner import ProcessScanner
from galactic_racer_trainer.drivers.memory_writer import MemoryWriter
from galactic_racer_trainer.overlay_core.overlay import OverlayWindow
from galactic_racer_trainer.feature_hub.base import BaseFeature

log = logging.getLogger("grt.registry")


class FeatureRegistry:
    def __init__(
        self,
        cfg: TrainerConfig,
        scanner: ProcessScanner,
        writer: MemoryWriter,
        overlay: OverlayWindow,
    ) -> None:
        self.cfg = cfg
        self.scanner = scanner
        self.writer = writer
        self.overlay = overlay
        self._features: dict[str, BaseFeature] = {}
        self._register_builtin()

    def _register_builtin(self) -> None:
        from galactic_racer_trainer.infinite_boost.module import InfiniteBoost
        from galactic_racer_trainer.speed_hack.module import SpeedHack
        from galactic_racer_trainer.credit_engine.module import CreditEngine
        from galactic_racer_trainer.esp_overlay.module import ESPOverlay

        for factory in (InfiniteBoost, SpeedHack, CreditEngine, ESPOverlay):
            feature = factory(self.cfg, self.scanner, self.writer, self.overlay)
            self._features[feature.name] = feature

    def enable_all(self, names: list[str]) -> None:
        for name in names:
            feature = self._features.get(name)
            if feature is None:
                log.warning("unknown feature: %s", name)
                continue
            try:
                feature.enable()
            except Exception as exc:  # noqa: BLE001
                log.exception("failed to enable %s: %s", name, exc)

    def disable_all(self) -> None:
        for feature in self._features.values():
            try:
                feature.disable()
            except Exception:  # noqa: BLE001
                pass

    @property
    def active_count(self) -> int:
        return sum(1 for f in self._features.values() if f.active)

    def register(self, name: str, factory: Callable[[], BaseFeature]) -> None:
        self._features[name] = factory()