# API (Phase I)

## Clock (abstract)
- `tick(dt: float) -> None`
- `read_time() -> float`
- `get_uncertainty() -> float`
- `get_metadata() -> dict`

## Comparison (dataclass)
- Fields: `label_a, label_b, time_s, t_a_s, t_b_s`
- Method: `.measure()` delegates to `analysis.compare_clocks(...)`

## analysis.py (pure functions)
- `run_clocks(clocks, duration, dt) -> dict[str, np.ndarray]`
- `compare_clocks(time_s, t_a_s, t_b_s) -> dict[str, float]`
- `plot_comparison(timeseries_dict, labels=None) -> None`
