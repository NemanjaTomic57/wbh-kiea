"""Small, file-I/O based bridge from the Python simulation to SWI-Prolog."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Iterable, Optional

from constants import MAP

ROOT = Path(__file__).resolve().parent
KNOWLEDGE_BASE = ROOT / "prolog_kb.pl"


class PrologBridge:
    """Exports current simulation facts and evaluates one deterministic query."""

    def __init__(self, executable: str = "swipl") -> None:
        configured = os.environ.get("SWIPL", executable)
        self.executable = shutil.which(configured)
        if self.executable is None:
            raise RuntimeError(
                "SWI-Prolog was not found. Install SWI-Prolog or set SWIPL to its executable."
            )

    @staticmethod
    def _map_facts() -> list[str]:
        facts: list[str] = []
        depot_id = goal_id = 0
        for y, row in enumerate(MAP):
            for x, cell in enumerate(row):
                if cell == "#":
                    facts.append(f"wall({x},{y}).")
                else:
                    facts.append(f"road({x},{y}).")
                if cell == "D":
                    facts.append(f"depot(d{depot_id},{x},{y}).")
                    depot_id += 1
                elif cell == "Z":
                    facts.append(f"goal(z{goal_id},{x},{y}).")
                    goal_id += 1
        return facts

    @staticmethod
    def _runtime_facts(agents: Iterable, task) -> list[str]:
        facts = PrologBridge._map_facts()
        for agent in agents:
            state = "idle" if agent.state.name == "IDLE" else "busy"
            facts.append(
                f"agent({agent.id},{agent.x},{agent.y},{agent.capacity},"
                f"{agent.battery},{state})."
            )
        facts.append(
            f"task({task.id},{task.depot_x},{task.depot_y},{task.dest_x},"
            f"{task.dest_y},{task.weight})."
        )
        return facts

    def _ask(self, query: str, agents=(), task=None) -> str:
        facts = self._map_facts() if task is None else self._runtime_facts(agents, task)
        with tempfile.NamedTemporaryFile("w", suffix=".pl", encoding="utf-8", delete=False) as handle:
            handle.write("\n".join(facts))
            fact_file = handle.name
        try:
            result = subprocess.run(
                [self.executable, "-q", "-s", str(KNOWLEDGE_BASE), "-s", fact_file,
                 "-g", query, "-t", "halt"],
                capture_output=True, text=True, check=True, timeout=10,
            )
            return result.stdout.strip()
        finally:
            Path(fact_file).unlink(missing_ok=True)

    def reachable(self, start: tuple[int, int], target: tuple[int, int]) -> bool:
        query = (
            f"(reachable(({start[0]},{start[1]}),({target[0]},{target[1]}))"
            " -> write(yes) ; write(no))"
        )
        return self._ask(query) == "yes"

    def candidate_agent(self, task, agents: Iterable) -> Optional[int]:
        query = f"(candidate_agent(task({task.id}), Agent) -> write(Agent) ; write(none))"
        answer = self._ask(query, agents, task)
        return None if answer == "none" else int(answer)
