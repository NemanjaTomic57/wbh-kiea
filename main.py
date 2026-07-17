import random
import time
from dataclasses import dataclass

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

def get_possible_moves(map_data, agent):
    matrix = [list(row) for row in map_data]

    # Check for left, up, right and down if there is a wall
    possible_moves = []
    if matrix[agent.y][agent.x-1] != "#":
        possible_moves.append("left")
    if matrix[agent.y-1][agent.x] != "#":
        possible_moves.append("up")
    if matrix[agent.y][agent.x+1] != "#":
        possible_moves.append("right")
    if matrix[agent.y+1][agent.x] != "#":
        possible_moves.append("down")

    return possible_moves

def manhattan(a, b):
    return sum(abs(x-y) for x, y in zip(a, b))

def move_agent(agent, possible_moves):
    move = random.sample(possible_moves, 1)
    
    match move[0]:
        case "left":
            agent.x -= 1
        case "up":
            agent.y -= 1
        case "right":
            agent.x += 1
        case "down":
            agent.y += 1
        case _:
            print(f"error -> could not determine move: {move}")
    print(f"Agent {agent.id} moved {move[0]}")

def main():
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

    agents = [standard_agent, express_agent]

    print_map(MAP, agents)

    print(get_depot_positions(MAP))

    for _ in range(5):
        time.sleep(1)
        for agent in agents:
            possible_moves = get_possible_moves(MAP, agent)
            move_agent(agent, possible_moves)

        # print_map(MAP, agents)
    print_map(MAP, agents)

if __name__ == "__main__":
    main()
