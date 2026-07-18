import random
import time
import heapq
from enum import Enum, auto
from dataclasses import field
from collections import deque
from dataclasses import dataclass
from typing import Optional

from agent import Agent, AgentState, create_agents
from task import Task, create_task
from map import *

def determine_winner(agents: list[Agent], task: Task) -> Optional[Agent]:
    candidates = [
        agent
        for agent in agents
        if agent.state == AgentState.IDLE
    ]

    if not candidates:
        return None

    return min(
        candidates,
        key=lambda agent: shortest_path(
            (agent.x, agent.y),
            (task.depot_x, task.depot_y),
        ),
    )

def perform_bidding(agents: list[Agent], tasks: list[Task]):
    for task in tasks:
        if task.agent_id is not None:
            continue

        winner = determine_winner(agents, task)

        if winner is None:
            continue

        task.agent_id = winner.id
        winner.assign_task(task)

        print(f"Task {task.id} assigned to Agent {winner.id}")

def main():
    tasks: list[Task] = []
    agents = create_agents(n=2)
    round = 0
    task_id = 0

    for _ in range(2):
        tasks.append(create_task(task_id))
        task_id += 1

    while True:
        perform_bidding(agents, tasks)

        for agent in agents:
            agent.update()

        print_map(MAP, agents)

        round += 1

        time.sleep(1)

    print_route(agents[0].route)

if __name__ == "__main__":
    main()
