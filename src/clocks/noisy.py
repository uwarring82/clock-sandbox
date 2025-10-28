"""NoisyOscillatorClock: white fractional-frequency noise y ~ N(0, sigma_y) at τ=1 s."""
from __future__ import annotations
from typing import Dict, Any, Optional
import numpy as np
from ..core import Clock


class NoisyOscillatorClock(Clock):
    """Elapsed time integrates dt * (1 + y_k), where y_k ~ N(0, sigma_y / sqrt(dt)).
    Phase I: white frequency noise only, parameterized by sigma_y at τ=1 s.
    Deterministic via NumPy Generator with seed.
    """

    def __init__(self, sigma_y: float = 1e-12, seed: Optional[int] = 0) -> None:
        self._elapsed_time: float = 0.0
        self._sigma_y = float(sigma_y)
        self._rng = np.random.default_rng(seed)

    def tick(self, dt: float) -> None:
        dt = float(dt)
        if dt <= 0:
            return
        std_y = self._sigma_y / (dt ** 0.5)  # scale to keep Allan @1s consistent (Phase I simplification)
        y = self._rng.normal(0.0, std_y)
        self._elapsed_time += dt * (1.0 + y)

    def read_time(self) -> float:
        return self._elapsed_time

    def get_uncertainty(self) -> float:
        # Approximate RMS time error over 1 s ≈ sigma_y [s] for small y.
        return self._sigma_y

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "type": "NoisyOscillatorClock",
            "description": "White fractional-frequency noise",
            "sigma_y_tau1s": self._sigma_y,
        }
