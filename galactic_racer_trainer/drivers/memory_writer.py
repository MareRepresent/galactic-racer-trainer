"""Thin safe wrapper around pymem writes with type checks."""
from __future__ import annotations

import struct
from typing import Any


class MemoryWriter:
    def __init__(self, handle: Any) -> None:
        if handle is None:
            raise ValueError("MemoryWriter requires an attached pymem handle")
        self.handle = handle

    def write_float(self, address: int, value: float) -> None:
        self.handle.write_float(address, float(value))

    def write_int(self, address: int, value: int) -> None:
        self.handle.write_int(address, int(value))

    def write_bytes(self, address: int, payload: bytes) -> None:
        self.handle.write_bytes(address, payload, len(payload))

    def nop(self, address: int, length: int) -> None:
        self.write_bytes(address, b"\x90" * length)

    def patch_jump(self, address: int, target: int) -> None:
        rel = target - (address + 5)
        self.write_bytes(address, b"\xE9" + struct.pack("<i", rel))