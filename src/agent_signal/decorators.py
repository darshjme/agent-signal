"""Decorators for signal-based agent coordination."""

from __future__ import annotations

from typing import Callable

from .registry import SignalRegistry


def on_signal(registry: SignalRegistry, signal_name: str) -> Callable:
    """
    Decorator that auto-connects the decorated function to a named signal.

    Usage::

        registry = SignalRegistry()

        @on_signal(registry, "task.completed")
        def handle_completion(task_id, result):
            print(f"Task {task_id} done: {result}")
    """
    def decorator(func: Callable) -> Callable:
        sig = registry.signal(signal_name)
        sig.connect(func)
        return func
    return decorator
