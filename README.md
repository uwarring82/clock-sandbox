# ClockSandbox

**Python infrastructure for simulating prototype clocks — from ideal models with tunable noise to global systems including GPS, VLBI Earth rotation, and pulsar timing.**

---

## Overview

**ClockSandbox** provides a modular environment to explore the physics, statistics, and network interactions of clocks across scales — from laboratory prototypes to astrophysical timekeepers.

The goal is to establish a **computational and conceptual sandbox** to test ideas about time measurement, stability, and synchronization:
- **Prototype clocks** with ideal and noisy oscillators
- **Noise models** (white, flicker, random walk, and custom spectra)
- **Networked clocks** with adaptive trust weights and feedback
- **External references** (GPS satellite timing, VLBI Earth rotation data, pulsar timing archives)

Ultimately, this sandbox aims to connect **quantum**, **geodetic**, and **astrophysical** clocks as complementary pillars of a metrological description of spacetime.

---

## Features (Planned)

- 🕰️ Modular `Clock` base class with selectable noise processes  
- 📈 Allan deviation, PSD, and correlation analysis tools  
- 🌍 Access layer for live GNSS and VLBI feeds (optional modules)  
- 🌌 Synthetic pulsar timing models and injected noise sequences  
- 🤝 Clock network simulation (trust weighting, consensus, resilience)  
- 📚 Jupyter notebooks for demonstrations and tutorials  

---

## Structure (to be implemented)

ClockSandbox/
├── src/
│   ├── clocks/              # clock models and noise generators
│   ├── networks/            # network simulation modules
│   └── data/                # example or live data interfaces
├── notebooks/               # demonstrations and analysis
├── docs/                    # conceptual background and references
└── LICENSES/                # MIT + CC-BY-4.0 text files

---

## Licensing

This project follows a dual-license model to encourage open scientific collaboration:

- **Code**: Released under the [MIT License](LICENSES/MIT_LICENSE.md)  
  *Permissive use for software, including modification and redistribution.*

- **Documentation and media**: Released under [Creative Commons Attribution 4.0 International (CC-BY 4.0)](LICENSES/CC_BY_4.0.md)  
  *Free use with attribution; ideal for teaching and academic reuse.*

---

## Citation

If you use this repository or derivative work in your research or teaching, please cite as:

> Warring, U. (2025). *ClockSandbox: A modular framework for simulating prototype and networked clocks across physical regimes.*  
> University of Freiburg. GitHub Repository.  
> [https://github.com/<your-github-handle>/ClockSandbox](https://github.com/)

---

## Vision

> *From quantum oscillators to cosmic beacons — exploring how clocks define and connect spacetime.*

The long-term vision is to establish an open, extensible platform where the community can model, analyze, and compare clocks as **physical systems**, **information sources**, and **metrological anchors**.  
ClockSandbox is an early step toward that foundation.

---

## Contributing

Contributions are welcome. Please open an issue or pull request if you:
- Implement new noise models or clock types  
- Add example notebooks or documentation  
- Propose connections to external timing data (GPS, VLBI, pulsars)

---

© 2025 Ulrich Warring.  
Released under the MIT License (software) and CC-BY 4.0 License (documentation).

## Quick Start

```bash
# 1) Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install dependencies (pinning minimal versions)
pip install -r requirements.txt

# 3) Run the Phase I example (prints metrics and produces plots)
PYTHONPATH=. MPLBACKEND=Agg python examples/basic_comparison.py

# 4) Optional: open and run the smoke-test notebook
jupyter lab notebooks/PhaseI_smoke_test.ipynb
```

Notes
- All times are in seconds; epoch (t_0 = 0).
- NoisyOscillatorClock is deterministic with a fixed seed (re-running yields identical outputs).

## Launch in Binder

[![Binder - JupyterLab](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/uwarring82/clock-sandbox/main?urlpath=lab)

- [Launch smoke test in Binder](https://mybinder.org/v2/gh/uwarring82/clock-sandbox/main?labpath=notebooks%2FPhaseI_smoke_test.ipynb)

