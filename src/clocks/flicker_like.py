"""Flicker-like fractional-frequency noise clock using a simple IIR model."""
from __future__ import annotations

from typing import Any, Dict, Optional

import numpy as np

from ..core import Clock


class FlickerLikeFreqClock(Clock):
    """Clock with low-order IIR flicker-like fractional-frequency noise."""

    def __init__(self, sigma_w: float = 5e-12, a: float = 1e-3, seed: Optional[int] = 0) -> None:
        if not 0.0 < a < 1.0:
            raise ValueError("a must be between 0 and 1")
        self._elapsed_time = 0.0
        self._y = 0.0
        self._sigma_w = float(sigma_w)
        self._a = float(a)
        self._rng = np.random.default_rng(seed)

    def tick(self, dt: float) -> None:
        dt = float(dt)
        if dt <= 0.0:
            return
        n = self._rng.normal(0.0, self._sigma_w / np.sqrt(dt))
        self._y = (1.0 - self._a) * self._y + self._a * n
        self._elapsed_time += dt * (1.0 + self._y)

    def read_time(self) -> float:
        return self._elapsed_time

    def get_uncertainty(self) -> float:
        return self._sigma_w

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "type": "FlickerLikeFreqClock",
            "description": "IIR-approximated flicker-like fractional-frequency noise",
            "sigma_w_tau1s": self._sigma_w,
            "a": self._a,
        }
