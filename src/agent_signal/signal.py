"""Signal — a named event channel for agent coordination."""

from __future__ import annotations

import threading
from typing import Callable, Any


class Signal:
    """A named event channel. Producers emit, consumers connect handlers."""

    def __init__(self, name: str) -> None:
        self._name = name
        self._handlers: list[Callable] = []
        self._lock = threading.Lock()

    @property
    def name(self) -> str:
        return self._name

    @property
    def handler_count(self) -> int:
        with self._lock:
            return len(self._handlers)

    def connect(self, handler: Callable) -> None:
        """Subscribe a handler to this signal."""
        if not callable(handler):
            raise TypeError(f"handler must be callable, got {type(handler)}")
        with self._lock:
            if handler not in self._handlers:
                self._handlers.append(handler)

    def disconnect(self, handler: Callable) -> None:
        """Unsubscribe a handler from this signal."""
        with self._lock:
            try:
                self._handlers.remove(handler)
            except ValueError:
                pass  # handler not connected — silent no-op

    def emit(self, *args: Any, **kwargs: Any) -> None:
        """Call all connected handlers synchronously."""
        with self._lock:
            handlers = list(self._handlers)
        for handler in handlers:
            handler(*args, **kwargs)

    def emit_async(self, *args: Any, **kwargs: Any) -> list[threading.Thread]:
        """Call all connected handlers in separate threads (non-blocking)."""
        with self._lock:
            handlers = list(self._handlers)
        threads = []
        for handler in handlers:
            t = threading.Thread(target=handler, args=args, kwargs=kwargs, daemon=True)
            t.start()
            threads.append(t)
        return threads

    def clear(self) -> None:
        """Disconnect all handlers."""
        with self._lock:
            self._handlers.clear()

    def __repr__(self) -> str:
        return f"Signal(name={self._name!r}, handlers={self.handler_count})"
