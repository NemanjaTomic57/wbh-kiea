import random
import time
from dataclasses import dataclass
from typing import Optional

GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"

MAP = (
    "##########################",
    "#........................#",
    "#....#..Z....D.....####..#",
    "#....#.......#........#.Z#",
    "#....######..#........#..#",
    "#............#........#..#",
    "#............#######..#..#",
    "#######..#............#..#",
    "#.Z......#...............#",
    "#........####......#######",
    "#....#...#Z.#............#",
    "#....#...#..#...###......#",
    "#....#...#..#.....#......#",
    "######...#..#.....#....D.#",
    "#......D.#........#####..#",
    "#........#####...........#",
    "##########################"
)

@dataclass
class Task:
    id: int
    depot_x: int
    depot_y: int
    dest_x: int
    dest_y: int
    agent_id: Optional[int] = None

@dataclass
class Agent:
    id: int
    x: int
    y: int
    speed: int
    capacity: int
    battery: int
    color: str

class StandardAgent(Agent):
    def __init__(self, id: int, x: int, y: int):
        super().__init__(
            id=id,
            x=x,
            y=y,
            speed=1,
            capacity=5,
            battery=100,
            color=GREEN
        )

class ExpressAgent(Agent):
    def __init__(self, id: int, x: int, y: int):
        super().__init__(
            id=id,
            x=x,
            y=y,
            speed=2,
            capacity=3,
            battery=80,
            color=RED
        )

def print_map(map_data, agents):
    rendered_map = [list(row) for row in map_data]

    for agent in agents:
        rendered_map[agent.y][agent.x] = (
            f"{agent.color}{agent.id}{RESET}"
        )

    for row in rendered_map:
        print(" ".join(row))

def create_agents():
    positions = random.sample(get_free_positions(MAP), 2)
    standard_agent = StandardAgent(
        id=0,
        x=positions[0][0],
        y=positions[0][1]
    )
    express_agent = ExpressAgent(
        id=1,
        x=positions[1][0],
        y=positions[1][1]
    )
    return [standard_agent, express_agent]

def get_free_positions(map_data):
    return [
        (x, y)
        for y, row in enumerate(map_data)
        for x, cell in enumerate(row)
        if cell == "."
    ]

def get_depot_positions(map_data):
    return [
        (x, y)
        for y, row in enumerate(map_data)
        for x, cell in enumerate(row)
        if cell == "D"
    ]

def get_destination_positions(map_data):
    return [
        (x, y)
        for y, row in enumerate(map_data)
        for x, cell in enumerate(row)
        if cell == "Z"
    ]

def manhattan(a, b):
    return sum(abs(x-y) for x, y in zip(a, b))

def deploy_package(id):
    depots = get_depot_positions(MAP)
    destinations = get_destination_positions(MAP)
    
    depot_x, depot_y = random.sample(depots, k=1)[0]
    dest_x, dest_y = random.sample(destinations, k=1)[0]

    print(
        f"ANNOUNCE(task_id={id}, "
        f"depot=({depot_x}, {depot_y}), "
        f"dest=({dest_x}, {dest_y}))"
    )
    package = Task(
        id=id,
        depot_x=depot_x,
        depot_y=depot_y,
        dest_x=dest_x,
        dest_y=dest_y
    )
    return package

def perform_bidding(agents, tasks):
    unassigned_tasks = [t for t in tasks if t.agent_id == None]

    for task in unassigned_tasks:
        print(task)

def main():
    tasks: list[Task] = []
    agents = create_agents()
    round = 0
    task_id = 0

    while True:
        time.sleep(1)
        round += 1

        if round % 2 == 0:
            tasks.append(deploy_package(task_id))
            perform_bidding(agents, tasks)
            task_id += 1

if __name__ == "__main__":
    main()
