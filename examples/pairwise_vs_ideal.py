"""Pairwise comparisons between noisy clocks and an ideal reference."""
from __future__ import annotations

from src.analysis import compare_clocks, plot_comparison, run_clocks
from src.clocks.flicker_like import FlickerLikeFreqClock
from src.clocks.ideal import IdealClock
from src.clocks.random_walk import RandomWalkFreqClock


def main() -> None:
    ideal = IdealClock()
    rw = RandomWalkFreqClock(sigma_rw=2e-14, seed=123)
    fl = FlickerLikeFreqClock(sigma_w=5e-12, a=1e-3, seed=456)

    duration = 86_400.0
    dt = 1.0

    ts_rw = run_clocks([ideal, rw], duration=duration, dt=dt)
    metrics_rw = compare_clocks(ts_rw["time"], ts_rw["clock_0"], ts_rw["clock_1"])
    print("=== Ideal vs Random-Walk ===")
    for key, value in metrics_rw.items():
        print(f"{key}: {value:.6e}")

    ideal2 = IdealClock()
    ts_fl = run_clocks([ideal2, fl], duration=duration, dt=dt)
    metrics_fl = compare_clocks(ts_fl["time"], ts_fl["clock_0"], ts_fl["clock_1"])
    print("\n=== Ideal vs Flicker-like ===")
    for key, value in metrics_fl.items():
        print(f"{key}: {value:.6e}")

    plot_comparison(ts_rw, labels=["Ideal", "Random-Walk"])
    plot_comparison(ts_fl, labels=["Ideal", "Flicker-like"])


if __name__ == "__main__":
    main()
