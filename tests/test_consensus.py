"""Tests for consensus helpers."""
from __future__ import annotations

from src.analysis import consensus_weighted_average, run_clocks
from src.clocks.flicker_like import FlickerLikeFreqClock
from src.clocks.ideal import IdealClock
from src.clocks.noisy import NoisyOscillatorClock
from src.clocks.random_walk import RandomWalkFreqClock


def test_consensus_weights_sum_to_one() -> None:
    ideal = IdealClock()
    white = NoisyOscillatorClock(sigma_y=1e-11, seed=1)
    rw = RandomWalkFreqClock(sigma_rw=2e-14, seed=2)
    fl = FlickerLikeFreqClock(sigma_w=5e-12, a=1e-3, seed=3)
    ts = run_clocks([ideal, white, rw, fl], duration=100.0, dt=1.0)
    consensus = consensus_weighted_average(ts, ["clock_1", "clock_2", "clock_3"])
    assert abs(sum(consensus["weights"]) - 1.0) < 1e-12
