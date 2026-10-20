# Contributing to galactic-racer-trainer

Thanks for helping improve the STAR WARS: Galactic Racer Trainer toolkit.

## Ground rules
- Educational / single-player use only. Do not use in online or ranked lobbies.
- Never commit live process handles, dumps, or copyrighted game assets.
- Keep feature modules under `galactic_racer_trainer/<feature_name>/module.py`
  and register them in `feature_hub/registry.py`.

## Local dev
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py --config config/trainer.toml
```

## Adding a feature
1. Subclass `BaseFeature`, set `name`, implement `tick()`.
2. Register it in `FeatureRegistry._register_builtin`.
3. Add pointers/offsets under `[pointers]` / `[offsets]` in `config/trainer.toml`.
4. Add a test under `tests/`.

## Style
- Ruff + mypy clean. Type hints required on public APIs.
- Keep `tick()` under ~5 ms; heavy work goes off-thread.

## PRs
Small, focused, with a short writeup of what pointer signature you found and how you verified it.