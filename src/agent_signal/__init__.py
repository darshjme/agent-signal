"""agent-signal: Event signaling and pub/sub for agent coordination."""

from .signal import Signal
from .registry import SignalRegistry
from .bus import EventBus
from .decorators import on_signal

__all__ = ["Signal", "SignalRegistry", "EventBus", "on_signal"]
__version__ = "1.0.0"
