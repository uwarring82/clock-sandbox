# Design Decisions — Phase I

- Keep **core.py** stdlib-only (no NumPy); analysis and implementations may use NumPy.
- Provide **deterministic runs** via explicit seeds.
- Comparison logic lives in **pure functions**; the `Comparison` class only delegates.
- Exclude real-time daemons, networking, live data, and complex noise for Phase I.
- Phase II will consider Allan deviation, additional noise processes, disciplining, and adapters.
