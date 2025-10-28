"""Analysis utilities (pure functions): run and compare clocks."""
from __future__ import annotations
from typing import List, Dict
import numpy as np
from .core import Clock


def run_clocks(clocks: List[Clock], duration: float, dt: float) -> Dict[str, np.ndarray]:
    """Run multiple clocks in parallel with deterministic stepping (virtual time).
    Returns dict: 'time', 'clock_0', 'clock_1', ...
    """
    duration = float(duration); dt = float(dt)
    if dt <= 0 or duration <= 0:
        raise ValueError("duration and dt must be > 0")
    n_steps = int(round(duration / dt))
    time = np.linspace(0.0, n_steps * dt, n_steps + 1, dtype=float)
    traces = [np.zeros(n_steps + 1, dtype=float) for _ in clocks]

    # initial read before ticking
    for i, c in enumerate(clocks):
        traces[i][0] = c.read_time()

    # advance
    for k in range(1, n_steps + 1):
        for c in clocks:
            c.tick(dt)
        for i, c in enumerate(clocks):
            traces[i][k] = c.read_time()

    out = {"time": time}
    for i, arr in enumerate(traces):
        out[f"clock_{i}"] = arr
    return out


def compare_clocks(time_s, t_a_s, t_b_s) -> Dict[str, float]:
    """Simple metrics between two elapsed-time series (seconds).
    Returns mean_offset [s], std_offset [s], max_abs_error [s], final_drift_rate [s/s].
    """
    t = np.asarray(time_s, dtype=float)
    a = np.asarray(t_a_s, dtype=float)
    b = np.asarray(t_b_s, dtype=float)
    if t.size != a.size or t.size != b.size:
        raise ValueError("time, a, b lengths must match")
    diff = b - a
    mean_offset = float(np.mean(diff))
    std_offset = float(np.std(diff, ddof=1)) if diff.size > 1 else 0.0
    max_abs_error = float(np.max(np.abs(diff)))
    final_drift_rate = float((diff[-1] - diff[0]) / (t[-1] - t[0])) if t[-1] > t[0] else 0.0
    return {
        "mean_offset_s": mean_offset,
        "std_offset_s": std_offset,
        "max_abs_error_s": max_abs_error,
        "final_drift_rate_s_per_s": final_drift_rate,
    }


def plot_comparison(timeseries_dict: Dict[str, np.ndarray], labels=None) -> None:
    """Matplotlib plot: (1) elapsed time, (2) first pair difference."""
    import matplotlib.pyplot as plt
    t = timeseries_dict["time"]
    keys = [k for k in timeseries_dict if k.startswith("clock_")]
    if labels is None:
        labels = keys

    plt.figure()
    for k, lab in zip(keys, labels):
        plt.plot(t, timeseries_dict[k], label=lab)
    plt.xlabel("Simulation time [s]")
    plt.ylabel("Elapsed time reading [s]")
    plt.title("Clock readings")
    plt.legend()

    if len(keys) >= 2:
        diff = timeseries_dict[keys[1]] - timeseries_dict[keys[0]]
        plt.figure()
        plt.plot(t, diff)
        plt.xlabel("Simulation time [s]")
        plt.ylabel(f"{labels[1]} - {labels[0]} [s]")
        plt.title("Time difference")
    plt.show()
