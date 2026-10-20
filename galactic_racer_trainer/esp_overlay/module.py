"""ESP overlay — draws racer positions & track markers via the overlay window."""
from __future__ import annotations

from galactic_racer_trainer.feature_hub.base import BaseFeature


class ESPOverlay(BaseFeature):
    name = "esp_overlay"

    def tick(self) -> None:
        racers = self.scanner.resolve(
            self.cfg.pointers.get("racer_list", 0x0),
            self.cfg.offsets.get("racer_chain", [0x0]),
        )
        # placeholder: real implementation hooks the render pipeline
        self.overlay.set_status(f"ESP racers @ 0x{racers:X}")