from pathlib import Path

from galactic_racer_trainer.config.loader import load_config


def test_missing_config_returns_defaults(tmp_path: Path):
    cfg = load_config(tmp_path / "missing.toml")
    assert cfg.target_process == "GalacticRacer.exe"
    assert cfg.overlay.enabled is True


def test_loads_profile_from_disk(tmp_path: Path):
    p = tmp_path / "trainer.toml"
    p.write_text(
        'profile = "hardcore"\n'
        'target_process = "GalacticRacer.exe"\n'
        'enabled_features = ["speed_hack"]\n'
        '[overlay]\nenabled = false\nopacity = 0.5\n'
    )
    cfg = load_config(p)
    assert cfg.profile == "hardcore"
    assert cfg.enabled_features == ["speed_hack"]
    assert cfg.overlay.enabled is False