"""SignalRegistry — manages named signals for agent coordination."""

from __future__ import annotations

import threading
from typing import Any

from .signal import Signal


class SignalRegistry:
    """Central registry of named signals. Thread-safe."""

    def __init__(self) -> None:
        self._signals: dict[str, Signal] = {}
        self._lock = threading.Lock()

    def signal(self, name: str) -> Signal:
        """Return existing signal or create a new one."""
        with self._lock:
            if name not in self._signals:
                self._signals[name] = Signal(name)
            return self._signals[name]

    def emit(self, name: str, *args: Any, **kwargs: Any) -> None:
        """Emit a named signal. No-op if signal not registered."""
        with self._lock:
            sig = self._signals.get(name)
        if sig is not None:
            sig.emit(*args, **kwargs)

    def list_signals(self) -> list[str]:
        """Return sorted list of registered signal names."""
        with self._lock:
            return sorted(self._signals.keys())

    def clear_all(self) -> None:
        """Clear all signals and their handlers."""
        with self._lock:
            for sig in self._signals.values():
                sig.clear()
            self._signals.clear()

    def __repr__(self) -> str:
        return f"SignalRegistry(signals={self.list_signals()})"
