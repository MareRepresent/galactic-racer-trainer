"""Transparent overlay using tkinter — status text + hotkey toggle."""
from __future__ import annotations

import logging
import tkinter as tk

from galactic_racer_trainer.config.loader import OverlayConfig

log = logging.getLogger("grt.overlay")


class OverlayWindow:
    def __init__(self, cfg: OverlayConfig) -> None:
        self.cfg = cfg
        self._root: tk.Tk | None = None
        self._label: tk.Label | None = None
        self._text = "STAR WARS: Galactic Racer Trainer"

    def spawn(self) -> None:
        if not self.cfg.enabled:
            return
        try:
            self._root = tk.Tk()
            self._root.overrideredirect(True)
            self._root.attributes("-topmost", True)
            self._root.attributes("-alpha", self.cfg.opacity)
            self._label = tk.Label(
                self._root,
                text=self._text,
                fg="#FFE81F",
                bg="#000000",
                font=("Consolas", int(12 * self.cfg.font_scale)),
            )
            self._label.pack()
            self._root.geometry("+24+24")
        except Exception as exc:  # noqa: BLE001
            log.warning("overlay spawn failed: %s", exc)

    def set_status(self, text: str) -> None:
        self._text = text
        if self._label is not None:
            self._label.config(text=text)

    def close(self) -> None:
        if self._root is not None:
            try:
                self._root.destroy()
            except Exception:  # noqa: BLE001
                pass
            self._root = None