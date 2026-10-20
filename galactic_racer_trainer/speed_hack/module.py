"""Speed hack — multiplies velocity in the physics tick."""
from __future__ import annotations

from galactic_racer_trainer.feature_hub.base import BaseFeature


class SpeedHack(BaseFeature):
    name = "speed_hack"

    def tick(self) -> None:
        ptr = self.cfg.pointers.get("velocity")
        if ptr is None:
            return
        addr = self.scanner.resolve(ptr, self.cfg.offsets.get("velocity_chain", [0x0]))
        base_speed = self.cfg.offsets.get("base_speed", 320.0)
        self.writer.write_float(addr, float(base_speed) * 2.5)