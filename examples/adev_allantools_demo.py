"""Demo: Overlapping Allan deviation with uncertainties via allantools."""
from __future__ import annotations

from src.clocks.ideal import IdealClock
from src.clocks.noisy import NoisyOscillatorClock
from src.analysis import (
    run_clocks,
    fractional_frequency_from_time,
    adev_overlapping_allantools,
    plot_adev_with_uncertainties,
)

def main() -> None:
    ideal = IdealClock()
    noisy = NoisyOscillatorClock(sigma_y=1e-11, seed=101)
    duration = 24 * 3600.0
    dt = 1.0

    ts = run_clocks([ideal, noisy], duration=duration, dt=dt)
    t = ts["time"]
    x_noisy = ts["clock_1"]
    y = fractional_frequency_from_time(t, x_noisy, dt=dt)

    taus = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
    taus_s, adev, adev_err = adev_overlapping_allantools(y, dt=dt, taus=taus)
    print("tau [s]   adev       +/- 1σ")
    for tau, a, e in zip(taus_s, adev, adev_err):
        print(f"{tau:6.0f}  {a:9.3e}  ± {e:9.3e}")

    plot_adev_with_uncertainties(taus_s, adev, adev_err)


if __name__ == "__main__":
    main()
