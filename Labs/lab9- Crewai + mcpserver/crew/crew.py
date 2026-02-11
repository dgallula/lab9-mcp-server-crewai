"""Minimal CrewAI-like orchestrator.

This is a tiny orchestrator for educational purposes that runs a single agent in order.
It intentionally avoids non-determinism and external dependencies.
"""
from typing import Any


class Crew:
    """Simple crew that runs tasks in sequence."""

    def __init__(self):
        self.components = []

    def add(self, component: Any):
        self.components.append(component)

    def run(self):
        results = {}
        for comp in self.components:
            # We expect components to expose a `run()` method
            if hasattr(comp, "run"):
                results[comp.__class__.__name__] = comp.run()
        return results
