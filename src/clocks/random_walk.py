"""Random-walk fractional-frequency clock model."""
from __future__ import annotations

from typing import Any, Dict, Optional

import numpy as np

from ..core import Clock


class RandomWalkFreqClock(Clock):
    """Clock whose fractional frequency follows a random walk."""

    def __init__(self, sigma_rw: float = 1e-14, seed: Optional[int] = 0) -> None:
        self._elapsed_time = 0.0
        self._y = 0.0
        self._sigma_rw = float(sigma_rw)
        self._rng = np.random.default_rng(seed)

    def tick(self, dt: float) -> None:
        dt = float(dt)
        if dt <= 0.0:
            return
        self._y += self._rng.normal(0.0, self._sigma_rw * np.sqrt(dt))
        self._elapsed_time += dt * (1.0 + self._y)

    def read_time(self) -> float:
        return self._elapsed_time

    def get_uncertainty(self) -> float:
        return self._sigma_rw

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "type": "RandomWalkFreqClock",
            "description": "Fractional frequency performs a random walk",
            "sigma_rw_per_sqrt_s": self._sigma_rw,
        }
