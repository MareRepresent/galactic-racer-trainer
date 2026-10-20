"""Background daemon that toggles the overlay on the configured hotkey."""
from __future__ import annotations

import logging

try:
    import keyboard
except ImportError:  # pragma: no cover
    keyboard = None

from galactic_racer_trainer.config.loader import load_config
from galactic_racer_trainer.overlay_core.overlay import OverlayWindow

log = logging.getLogger("grt.hotkeys")


def run(config_path: str = "config/trainer.toml") -> None:
    if keyboard is None:
        log.error("install `keyboard` to use the hotkey daemon")
        return
    cfg = load_config(__import__("pathlib").Path(config_path))
    overlay = OverlayWindow(cfg.overlay)
    overlay.spawn()

    def toggle() -> None:
        if overlay._root is None:
            overlay.spawn()
        else:
            overlay.close()

    keyboard.add_hotkey(cfg.overlay.hotkey_toggle.lower(), toggle)
    log.info("hotkey daemon listening on %s", cfg.overlay.hotkey_toggle)
    keyboard.wait()


if __name__ == "__main__":
    run()