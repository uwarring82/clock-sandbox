"""IdealClock: perfect timekeeper baseline for interface proof."""
from __future__ import annotations
from typing import Dict, Any
from ..core import Clock


class IdealClock(Clock):
    def __init__(self) -> None:
        self._elapsed_time: float = 0.0

    def tick(self, dt: float) -> None:
        self._elapsed_time += float(dt)

    def read_time(self) -> float:
        return self._elapsed_time

    def get_uncertainty(self) -> float:
        return 0.0

    def get_metadata(self) -> Dict[str, Any]:
        return {"type": "IdealClock", "description": "Perfect reference clock"}
