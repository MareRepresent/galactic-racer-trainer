"""Infinite Boost — keeps the pod racer's boost meter pinned at max."""
from __future__ import annotations

from galactic_racer_trainer.feature_hub.base import BaseFeature


class InfiniteBoost(BaseFeature):
    name = "infinite_boost"

    def tick(self) -> None:
        ptr = self.cfg.pointers.get("boost_meter")
        if ptr is None:
            return
        addr = self.scanner.resolve(ptr, self.cfg.offsets.get("boost_chain", [0x0]))
        self.writer.write_float(addr, 100.0)