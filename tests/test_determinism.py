from src.analysis import compare_clocks, run_clocks
from src.clocks.ideal import IdealClock
from src.clocks.noisy import NoisyOscillatorClock


def test_noisy_determinism():
    a1 = IdealClock()
    b1 = NoisyOscillatorClock(sigma_y=1e-11, seed=42)
    ts1 = run_clocks([a1, b1], duration=100.0, dt=1.0)
    m1 = compare_clocks(ts1["time"], ts1["clock_0"], ts1["clock_1"])

    a2 = IdealClock()
    b2 = NoisyOscillatorClock(sigma_y=1e-11, seed=42)
    ts2 = run_clocks([a2, b2], duration=100.0, dt=1.0)
    m2 = compare_clocks(ts2["time"], ts2["clock_0"], ts2["clock_1"])

    assert m1 == m2, "Determinism failed: metrics differ for the same seed"
