"""Phase I demo: Ideal vs. Noisy clock over 1 day with 1 s steps."""
from __future__ import annotations
import pathlib
import sys

# Allow running as a script without installation
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.clocks.ideal import IdealClock
from src.clocks.noisy import NoisyOscillatorClock
from src.analysis import run_clocks, compare_clocks, plot_comparison
from src.core import Comparison

def main() -> None:
    ideal = IdealClock()
    noisy = NoisyOscillatorClock(sigma_y=1e-11, seed=42)  # visibly drifting vs ideal

    duration = 86_400.0  # 1 day
    dt = 1.0             # 1 s

    ts = run_clocks([ideal, noisy], duration=duration, dt=dt)
    metrics = compare_clocks(ts["time"], ts["clock_0"], ts["clock_1"])
    print("=== Comparison Metrics (Ideal -> Noisy) ===")
    for k, v in metrics.items():
        print(f"{k}: {v:.6e}")

    # Optional: assemble Comparison object (delegates to same function)
    cmp_obj = Comparison("Ideal", "Noisy", ts["time"].tolist(),
                         ts["clock_0"].tolist(), ts["clock_1"].tolist())
    assert metrics == cmp_obj.measure()  # should match exactly

    # Plot (close figures in headless runs)
    plot_comparison(ts, labels=["Ideal", "Noisy (white freq)"])

if __name__ == "__main__":
    main()
