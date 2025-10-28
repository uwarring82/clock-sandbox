"""
ClockSandbox core (Phase I)

- Minimal Clock ABC (pure stdlib).
- Thin Comparison dataclass delegating to analysis functions.
- Units: seconds; epoch t0 = 0 s.
- Readout = elapsed time since t0 (not cycles/radians).
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any


class Clock(ABC):
    """Abstract time-register representing an idealized timekeeper.

    Methods
    -------
    tick(dt): advance internal state by dt seconds.
    read_time(): return elapsed time [s] since t0.
    get_uncertainty(): return uncertainty [s] at τ=1 s (Phase I convention).
    get_metadata(): return descriptive metadata dict.
    """

    @abstractmethod
    def tick(self, dt: float) -> None:
        """Advance clock state by dt [s]."""
        raise NotImplementedError

    @abstractmethod
    def read_time(self) -> float:
        """Return elapsed time [s] since t0."""
        raise NotImplementedError

    @abstractmethod
    def get_uncertainty(self) -> float:
        """Return uncertainty [s] (τ=1 s convention for Phase I)."""
        raise NotImplementedError

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Return human-readable metadata."""
        raise NotImplementedError


@dataclass
class Comparison:
    """Container for two elapsed-time series (seconds) on a common grid."""

    label_a: str
    label_b: str
    time_s: List[float]
    t_a_s: List[float]
    t_b_s: List[float]

    def measure(self) -> Dict[str, float]:
        """Delegate to analysis.compare_clocks (keeps core stdlib-only)."""
        from . import analysis  # local import to avoid non-stdlib deps
        return analysis.compare_clocks(self.time_s, self.t_a_s, self.t_b_s)
