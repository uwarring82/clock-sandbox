# Design Decisions — Phase I

- Keep `src/core.py` stdlib-only (no NumPy).
- Deterministic runs via explicit seeds.
- Comparison logic lives in pure functions; `Comparison` only delegates.
- Exclude real-time daemons, networking, live data, and complex noise for Phase I.
- Phase II will add Allan deviation, additional noise processes, disciplining, and adapters.
