"""Triangular consensus example comparing three noisy clocks to an ideal reference."""
from __future__ import annotations

from src.analysis import compare_clocks, consensus_weighted_average, run_clocks
from src.clocks.flicker_like import FlickerLikeFreqClock
from src.clocks.ideal import IdealClock
from src.clocks.noisy import NoisyOscillatorClock
from src.clocks.random_walk import RandomWalkFreqClock


def main() -> None:
    ideal = IdealClock()
    white = NoisyOscillatorClock(sigma_y=1e-11, seed=11)
    rw = RandomWalkFreqClock(sigma_rw=2e-14, seed=22)
    fl = FlickerLikeFreqClock(sigma_w=5e-12, a=1e-3, seed=33)

    duration = 86_400.0
    dt = 1.0

    ts = run_clocks([ideal, white, rw, fl], duration=duration, dt=dt)
    keys = ["clock_1", "clock_2", "clock_3"]
    consensus = consensus_weighted_average(ts, keys, method="inv_var")

    print("=== Pairwise vs Ideal ===")
    labels = ["WhiteFreq", "RandomWalkFreq", "FlickerLikeFreq"]
    for idx, label in zip(range(1, 4), labels):
        metrics = compare_clocks(ts["time"], ts["clock_0"], ts[f"clock_{idx}"])
        formatted = {k: f"{v:.6e}" for k, v in metrics.items()}
        print(f"[{label}] {formatted}")

    consensus_metrics = compare_clocks(consensus["time"], ts["clock_0"], consensus["consensus"])
    print("\n=== Consensus vs Ideal (inverse-variance weights) ===")
    for key, value in consensus_metrics.items():
        print(f"{key}: {value:.6e}")

    assert abs(sum(consensus["weights"]) - 1.0) < 1e-12


if __name__ == "__main__":
    main()
