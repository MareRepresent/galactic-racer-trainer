# Pointer signatures (build 2026.03)

All addresses are **static offsets from `GalacticRacer.exe` base**.
Chains are resolved by `ProcessScanner.resolve(base, chain)`.

| Feature         | Base       | Chain          | Type    |
|-----------------|------------|----------------|---------|
| boost_meter     | 0x00B2F410 | `[0x18, 0x2C]` | float   |
| velocity        | 0x00B2F430 | `[0x10, 0x44]` | float   |
| credits         | 0x00C1A008 | `[0x00]`       | int32   |
| racer_list      | 0x00C1A120 | `[0x20, 0x08]` | pointer |

## Re-scanning after a patch
1. Launch the game, load into a race.
2. Run `python scripts/update_pointers.py`.
3. Any `FAILED` rows need a fresh AOB scan — see `docs/aob-scan.md`.