# AOB scan notes

When static offsets go stale after a game update, re-derive them with an
array-of-bytes scan against the module's `.text` section.

Typical pattern for the boost-meter writer:

```
F3 0F 11 83 ?? ?? ?? ?? 48 8B 5C 24
```

Use Cheat Engine's "Find what writes to this address" to grab the instruction,
then `pymem.pattern.pattern_scan_module` to find the instruction's address in
the current build. Convert the resulting VA to a static offset and update
`config/trainer.toml`.