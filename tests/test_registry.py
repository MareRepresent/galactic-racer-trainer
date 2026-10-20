from galactic_racer_trainer.feature_hub.registry import FeatureRegistry
from galactic_racer_trainer.config.loader import TrainerConfig


class _StubOverlay:
    def set_status(self, _text): ...
    def close(self): ...


class _StubScanner:
    def resolve(self, base, chain):
        return 0x1000


class _StubWriter:
    def write_float(self, *_): ...
    def write_int(self, *_): ...
    def write_bytes(self, *_): ...


def test_register_builtin_features():
    reg = FeatureRegistry(TrainerConfig(), _StubScanner(), _StubWriter(), _StubOverlay())
    assert "infinite_boost" in reg._features
    assert "speed_hack" in reg._features
    assert "credit_engine" in reg._features
    assert "esp_overlay" in reg._features


def test_unknown_feature_is_ignored():
    reg = FeatureRegistry(TrainerConfig(), _StubScanner(), _StubWriter(), _StubOverlay())
    reg.enable_all(["does_not_exist"])
    assert reg.active_count == 0