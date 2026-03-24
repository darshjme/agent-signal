"""EventBus — broadcast event bus with glob topic filtering."""

from __future__ import annotations

import fnmatch
import threading
from typing import Callable, Any


class EventBus:
    """Broadcast event bus. Topics support glob patterns (e.g. 'agent.*')."""

    def __init__(self) -> None:
        # maps pattern -> list of handlers
        self._subscriptions: dict[str, list[Callable]] = {}
        self._lock = threading.Lock()

    def subscribe(self, topic: str, handler: Callable) -> None:
        """Subscribe handler to topic. Topic may be a glob pattern."""
        if not callable(handler):
            raise TypeError(f"handler must be callable, got {type(handler)}")
        with self._lock:
            if topic not in self._subscriptions:
                self._subscriptions[topic] = []
            if handler not in self._subscriptions[topic]:
                self._subscriptions[topic].append(handler)

    def unsubscribe(self, topic: str, handler: Callable) -> None:
        """Unsubscribe handler from topic. Silent no-op if not found."""
        with self._lock:
            handlers = self._subscriptions.get(topic, [])
            try:
                handlers.remove(handler)
            except ValueError:
                pass
            if topic in self._subscriptions and not self._subscriptions[topic]:
                del self._subscriptions[topic]

    def publish(self, topic: str, data: dict | None = None) -> None:
        """Publish event to all handlers whose subscription pattern matches topic."""
        if data is None:
            data = {}
        with self._lock:
            # collect (pattern, handler) pairs where pattern matches topic
            matched: list[Callable] = []
            for pattern, handlers in self._subscriptions.items():
                if fnmatch.fnmatch(topic, pattern):
                    matched.extend(handlers)
        for handler in matched:
            handler(topic, data)

    def subscriber_count(self, topic: str | None = None) -> int:
        """
        Return total subscriber count across all patterns,
        or count of subscribers whose pattern matches the given topic.
        """
        with self._lock:
            if topic is None:
                return sum(len(h) for h in self._subscriptions.values())
            count = 0
            for pattern, handlers in self._subscriptions.items():
                if fnmatch.fnmatch(topic, pattern):
                    count += len(handlers)
            return count

    def __repr__(self) -> str:
        with self._lock:
            patterns = list(self._subscriptions.keys())
        return f"EventBus(patterns={patterns})"
