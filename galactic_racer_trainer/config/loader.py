"""TOML config loader with per-profile overrides."""
from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class OverlayConfig:
    enabled: bool = True
    opacity: float = 0.85
    hotkey_toggle: str = "F8"
    font_scale: float = 1.0


@dataclass
class TrainerConfig:
    profile: str = "default"
    target_process: str = "GalacticRacer.exe"
    enabled_features: list[str] = field(default_factory=list)
    overlay: OverlayConfig = field(default_factory=OverlayConfig)
    pointers: dict[str, int] = field(default_factory=dict)
    offsets: dict[str, int] = field(default_factory=dict)


def _coerce(raw: dict[str, Any]) -> TrainerConfig:
    overlay_raw = raw.pop("overlay", {}) or {}
    return TrainerConfig(
        profile=raw.get("profile", "default"),
        target_process=raw.get("target_process", "GalacticRacer.exe"),
        enabled_features=list(raw.get("enabled_features", [])),
        overlay=OverlayConfig(**overlay_raw),
        pointers=dict(raw.get("pointers", {})),
        offsets=dict(raw.get("offsets", {})),
    )


def load_config(path: Path) -> TrainerConfig:
    if not path.exists():
        return TrainerConfig()
    with path.open("rb") as fh:
        raw = tomllib.load(fh)
    return _coerce(raw)