# Security Policy

## Scope
This repository is a hobbyist single-player trainer for **STAR WARS: Galactic Racer**.
It attaches to the local game process on Windows and writes memory. That is its
entire purpose.

## Supported versions
| Trainer | Game build         | Status        |
|---------|--------------------|---------------|
| 1.4.x   | 2026.03            | Supported     |
| 1.3.x   | 2025.11            | Best effort   |

## Reporting a vulnerability
If you find:
- a memory-write primitive that can escape the target process,
- a way to get the trainer to load untrusted modules from a remote path,
- or a supply-chain issue in `requirements.txt`,

please open a **private** security advisory on GitHub (Security → Advisories).
Do not file a public issue for these.

## Explicit non-issues
- "It modifies the game" — yes, that is the point.
- "Anti-cheat detects it" — out of scope; do not use online.
- "It requires admin" — documented, expected on Windows for `OpenProcess`.

## Out-of-scope use
Using this against other players in multiplayer is prohibited by the project and
by the game's ToS. Reports of bans from online play will not be actioned.