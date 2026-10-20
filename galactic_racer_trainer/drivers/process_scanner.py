"""Locate the Galactic Racer process and grab a handle for memory access."""
from __future__ import annotations

import logging

try:
    import pymem
    import pymem.process
except ImportError:  # pragma: no cover - optional on non-Windows
    pymem = None

log = logging.getLogger("grt.drivers.scanner")


class ProcessScanner:
    def __init__(self, process_name: str) -> None:
        self.process_name = process_name
        self.handle = None
        self.base_module = None

    def attach(self) -> bool:
        if pymem is None:
            log.error("pymem unavailable — install requirements on Windows")
            return False
        try:
            self.handle = pymem.Pymem(self.process_name)
            self.base_module = pymem.process.module_from_name(
                self.handle.process_handle, self.process_name
            )
            log.info("attached to %s (base=0x%X)", self.process_name, self.base_module.lpBaseOfDll)
            return True
        except Exception as exc:  # noqa: BLE001
            log.warning("attach failed: %s", exc)
            return False

    def resolve(self, base_offset: int, chain: list[int]) -> int:
        """Follow a pointer chain starting at base_offset."""
        if self.handle is None or self.base_module is None:
            raise RuntimeError("not attached")
        addr = self.base_module.lpBaseOfDll + base_offset
        for off in chain[:-1]:
            addr = self.handle.read_longlong(addr) + off
        return addr + chain[-1]