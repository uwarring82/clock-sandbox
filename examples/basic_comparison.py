"""Phase I demo: Ideal vs Noisy over 1 day with 1 s steps (deterministic seed)."""
from __future__ import annotations
from src.clocks.ideal import IdealClock
from src.clocks.noisy import NoisyOscillatorClock
from src.analysis import run_clocks, compare_clocks, plot_comparison
from src.core import Comparison


def main() -> None:
    ideal = IdealClock()
    noisy = NoisyOscillatorClock(sigma_y=1e-11, seed=42)

    duration = 86_400.0  # 1 day
    dt = 1.0

    ts = run_clocks([ideal, noisy], duration=duration, dt=dt)
    metrics = compare_clocks(ts["time"], ts["clock_0"], ts["clock_1"])
    print("=== Comparison Metrics (Ideal -> Noisy) ===")
    for k, v in metrics.items():
        print(f"{k}: {v:.6e}")

    cmp_obj = Comparison("Ideal", "Noisy", ts["time"].tolist(),
                         ts["clock_0"].tolist(), ts["clock_1"].tolist())
    assert metrics == cmp_obj.measure()  # same numbers via delegation

    # Plot (optional; safe to comment in headless CI)
    plot_comparison(ts, labels=["Ideal", "Noisy (white freq)"])


if __name__ == "__main__":
    main()
