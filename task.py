import random
from dataclasses import field, dataclass
from typing import Optional

from map import *

@dataclass
class Task:
    id: int
    depot_x: int
    depot_y: int
    dest_x: int
    dest_y: int
    weight: int = 1
    agent_id: Optional[int] = None

def create_task(id):
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
        dest_y=dest_y,
        weight=1,
    )
    return package
