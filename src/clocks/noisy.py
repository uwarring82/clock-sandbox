"""NoisyOscillatorClock: white fractional-frequency noise y ~ N(0, sigma_y)."""
from __future__ import annotations
from typing import Dict, Any, Optional
import numpy as np
from ..core import Clock

class NoisyOscillatorClock(Clock):
    """Elapsed time integrates dt * (1 + y_k), where y_k ~ N(0, sigma_y) per 1 s sample.
    Phase I: white frequency noise only, parameterized by sigma_y at τ=1 s.
    Deterministic runs via NumPy Generator with given seed.
    """
    def __init__(self, sigma_y: float = 1e-12, seed: Optional[int] = 0) -> None:
        self._elapsed_time: float = 0.0
        self._sigma_y = float(sigma_y)
        # RNG for determinism
        self._rng = np.random.default_rng(seed)

        # For dt != 1 s, scale std of y by 1/sqrt(dt) so that Allan at 1 s matches sigma_y
        # (Simplified Phase I convention.)
    def tick(self, dt: float) -> None:
        dt = float(dt)
        if dt <= 0:
            return
        # White frequency noise scaling: std_y(dt) = sigma_y / sqrt(dt)
        std_y = self._sigma_y / np.sqrt(dt)
        y = self._rng.normal(loc=0.0, scale=std_y)
        self._elapsed_time += dt * (1.0 + y)

    def read_time(self) -> float:
        return self._elapsed_time

    def get_uncertainty(self) -> float:
        # Phase I: report characteristic 1-second instability as seconds of error over 1 s
        # For small y: time error over 1 s ≈ y * 1 s; RMS = sigma_y [s]
        return self._sigma_y

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "type": "NoisyOscillatorClock",
            "description": "White fractional-frequency noise",
            "sigma_y_tau1s": self._sigma_y,
        }
