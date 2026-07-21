"""Reproducible result evidence for the Prolog calls used by the simulation."""

from agent import ExpressAgent, StandardAgent
from prolog_bridge import PrologBridge
from task import Task


def main() -> None:
    # Valid positions from constants.MAP; the task uses the depot at (21, 3)
    # and the goal at (8, 2).  These are normal simulation objects, not
    # Prolog-only stand-ins.
    agents = [StandardAgent(0, 2, 2), ExpressAgent(1, 20, 3)]
    task = Task(7, depot_x=21, depot_y=3, dest_x=8, dest_y=2, weight=1)
    prolog = PrologBridge()

    reachable = prolog.reachable((task.depot_x, task.depot_y), (task.dest_x, task.dest_y))
    print("?- reachable((21,3),(8,2)).")
    print("true." if reachable else "false.")

    candidate = prolog.candidate_agent(task, agents)
    print(
        "?- task(7,21,3,8,2,1), agent(0,2,2,5,100,idle), "
        "agent(1,20,3,3,80,idle), candidate_agent(task(7), Agent)."
    )
    print(f"Agent = {candidate}." if candidate is not None else "false.")


if __name__ == "__main__":
    main()
