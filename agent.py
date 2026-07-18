import random
from enum import Enum, auto
from dataclasses import field, dataclass
from typing import Optional

from task import Task
from map import *
from constants import *

class AgentState(Enum):
    IDLE = auto()
    TO_DEPOT = auto()
    PICKING_UP = auto()
    TO_DESTINATION = auto()

@dataclass
class Agent:
    id: int
    x: int
    y: int
    speed: int
    capacity: int
    battery: int
    color: str

    state: AgentState = AgentState.IDLE

    task: Optional[Task] = None
    path: list[tuple[int, int]] = field(default_factory=list)
    pickup_timer: int = 0
    route: list[tuple[int, int]] = field(default_factory=list)

    def update(self):
        if self.task == None:
            return

        match self.state:
            case AgentState.IDLE:
                return
            
            case AgentState.TO_DEPOT:
                self.move_one_step()

                if (self.x, self.y) == (
                    self.task.depot_x,
                    self.task.depot_y,
                ):
                    self.state = AgentState.PICKING_UP
                    self.pickup_timer = 1

            case AgentState.PICKING_UP:
                self.pickup_timer -= 1

                if self.pickup_timer == 0:
                    self.path = shortest_path(
                        (self.x, self.y),
                        (self.task.dest_x, self.task.dest_y),
                    )

                    self.state = AgentState.TO_DESTINATION

            case AgentState.TO_DESTINATION:
                self.move_one_step()

                if (self.x, self.y) == (
                    self.task.dest_x,
                    self.task.dest_y,
                ):
                    self.finish_task()

    def assign_task(self, task: Task):
        self.task = task

        self.path = shortest_path(
            (self.x, self.y),
            (task.depot_x, task.depot_y),
        )

        self.route = [(self.x, self.y)]

        self.state = AgentState.TO_DEPOT

    def move_one_step(self):
        for _ in range(self.speed):
            if len(self.path) <= 1:
                return
            
            self.path.pop(0)
            self.x, self.y = self.path[0]
            self.route.append((self.x, self.y))

    def finish_task(self):
        if self.task == None:
            print(f"Error: Agent {self.id} does not have a task to return")
            return

        print(f"Agent {self.id} delivered task {self.task.id}")

        print_route(self.route)

        self.task = None
        self.path.clear()
        self.route.clear()

        self.state = AgentState.IDLE

class StandardAgent(Agent):
    def __init__(self, id: int, x: int, y: int):
        super().__init__(
            id=id,
            x=x,
            y=y,
            speed=1,
            capacity=5,
            battery=100,
            color=GREEN,
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
            color=RED,
        )

def create_agents(n: int):
    positions = random.sample(get_free_positions(MAP), n)
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
