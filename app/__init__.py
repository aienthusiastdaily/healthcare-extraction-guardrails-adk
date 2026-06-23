"""ADK app entrypoint."""

try:
    from .agent import root_agent
except ImportError:  # ADK eval imports this file directly from its path.
    from agent import root_agent

__all__ = ["root_agent"]
