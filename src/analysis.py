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


def fractional_frequency_from_time(time_s, elapsed_s, dt=None):
    """Compute fractional frequency y_k from elapsed time samples."""
    import numpy as np

    t = np.asarray(time_s, dtype=float)
    x = np.asarray(elapsed_s, dtype=float)
    if t.shape != x.shape:
        raise ValueError("time_s and elapsed_s must have the same shape")
    if t.size < 2:
        raise ValueError("need at least two samples to compute fractional frequency")

    dt_array = np.diff(t)
    if np.any(dt_array <= 0):
        raise ValueError("time grid must be strictly increasing")

    if dt is None:
        denom = dt_array
    else:
        denom = float(dt)
        if denom <= 0:
            raise ValueError("dt must be positive")
        if not np.allclose(dt_array, denom, rtol=1e-6, atol=0.0):
            raise ValueError("time grid spacing does not match provided dt")

    y = np.diff(x) / denom - 1.0
    return y


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


def consensus_weighted_average(timeseries_dict, keys, method="inv_var"):
    """Compute a simple consensus series via inverse-variance weighting."""
    t = timeseries_dict["time"]
    data = [timeseries_dict[k] for k in keys]
    arr = np.vstack(data)
    var = np.var(arr - arr.mean(axis=1, keepdims=True), axis=1, ddof=1)
    var = np.where(var <= 0.0, 1e-24, var)
    if method == "inv_var":
        w = 1.0 / var
        w = w / np.sum(w)
    else:
        raise ValueError(f"Unknown method: {method}")
    consensus = np.average(arr, axis=0, weights=w)
    return {"time": t, "consensus": consensus, "weights": w.tolist()}


# ===== Overlapping Allan deviation via allantools (Phase I+) =====
def adev_overlapping_allantools(y, dt, taus=None):
    """Compute overlapping Allan deviation using 'allantools' with uncertainties.

    Parameters
    ----------
    y : array-like
        Fractional frequency time series sampled uniformly every dt seconds.
    dt : float
        Sampling interval [s].
    taus : array-like or None
        Optional list/array of tau values [s]. If None, allantools will choose defaults.

    Returns
    -------
    taus_s : np.ndarray
        Tau values [s].
    adev : np.ndarray
        Overlapping Allan deviation σ_y(τ).
    adev_err : np.ndarray
        1-σ uncertainty estimates corresponding to σ_y(τ).
    """
    import numpy as np
    import allantools as at

    y = np.asarray(y, dtype=float)
    rate = 1.0 / float(dt)  # samples per second

    if taus is None:
        # Let allantools choose logarithmic tau sequence (overlapping)
        # Compute with oadev (overlapping Allan deviation) and data_type='freq'
        taus_s, adev, adev_err, _ = at.oadev(y, rate=rate, data_type='freq')
    else:
        taus_req = np.asarray(taus, dtype=float)
        if np.any(taus_req <= 0):
            raise ValueError("taus must be positive")
        # allantools interprets 'taus' directly in seconds when rate is provided
        taus_s, adev, adev_err, _ = at.oadev(y, rate=rate, data_type='freq', taus=taus_req)
    return np.asarray(taus_s, float), np.asarray(adev, float), np.asarray(adev_err, float)


def plot_adev_with_uncertainties(taus_s, adev, adev_err, title="Overlapping Allan deviation (allantools)"):
    """Log-log plot of ADEV with 1-σ error bars."""
    import matplotlib.pyplot as plt
    import numpy as np

    plt.figure()
    yerr = adev_err
    # Avoid non-positive values on log scale; mask zeros if any
    mask = (taus_s > 0) & (adev > 0)
    plt.errorbar(taus_s[mask], adev[mask], yerr=yerr[mask], fmt='o', capsize=3)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("τ [s]")
    plt.ylabel("σ_y(τ)")
    plt.title(title)
    plt.grid(True, which="both", ls=":")
    plt.show()
