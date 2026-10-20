"""Base class all trainer features inherit from."""
from __future__ import annotations

import abc
import threading

from galactic_racer_trainer.config.loader import TrainerConfig
from galactic_racer_trainer.drivers.process_scanner import ProcessScanner
from galactic_racer_trainer.drivers.memory_writer import MemoryWriter
from galactic_racer_trainer.overlay_core.overlay import OverlayWindow


class BaseFeature(abc.ABC):
    name: str = "base"

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
        self.active = False
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()

    @abc.abstractmethod
    def tick(self) -> None:
        """Called on each loop iteration while active."""

    def enable(self) -> None:
        if self.active:
            return
        self.active = True
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, name=f"grt-{self.name}", daemon=True)
        self._thread.start()

    def disable(self) -> None:
        self.active = False
        self._stop.set()

    def _loop(self) -> None:
        while not self._stop.is_set():
            try:
                self.tick()
            except Exception:  # noqa: BLE001
                pass
            self._stop.wait(0.033)