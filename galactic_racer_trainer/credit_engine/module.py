"""Credit engine — patches the racer's credit balance on demand."""
from __future__ import annotations

from galactic_racer_trainer.feature_hub.base import BaseFeature


class CreditEngine(BaseFeature):
    name = "credit_engine"

    def tick(self) -> None:
        addr = self.cfg.pointers.get("credits")
        if addr is None:
            return
        target = self.cfg.offsets.get("credit_target", 999_999)
        self.writer.write_int(self.scanner.resolve(addr, [0x0]), int(target))