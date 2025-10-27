"""
ClockSandbox core (Phase I)

- Defines the minimal Clock protocol (abstract base class).
- Defines a thin Comparison dataclass that delegates metrics to analysis functions.
- Units: seconds. Epoch t0 = 0 s. Readout is elapsed time (not cycles/radians).
- Fractional frequency y(t) is dimensionless (handled in implementations).
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any

class Clock(ABC):
    """Abstract time-register representing an idealized timekeeper.
    Methods:
      - tick(dt): advance internal state by dt seconds.
      - read_time(): return elapsed time [s] since t0.
      - get_uncertainty(): return a physically motivated uncertainty [s] for τ=1 s (Phase I).
      - get_metadata(): return descriptive metadata dict.
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
        """Return uncertainty [s] (Phase I convention: estimate at τ=1 s)."""
        raise NotImplementedError

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Return a dict with human-readable metadata."""
        raise NotImplementedError


@dataclass
class Comparison:
    """Thin container for two elapsed-time series (seconds) sampled on a common time grid."""
    label_a: str
    label_b: str
    time_s: List[float]        # common sampling times
    t_a_s: List[float]         # readings of clock A
    t_b_s: List[float]         # readings of clock B

    def measure(self) -> Dict[str, float]:
        """Delegate to analysis.compare_clocks to compute metrics."""
        # Local import to keep core.py stdlib-only
        from . import analysis
        return analysis.compare_clocks(self.time_s, self.t_a_s, self.t_b_s)
