import heapq

from constants import *

def print_map(map_data, agents):
    rendered_map = [list(row) for row in map_data]

    for agent in agents:
        rendered_map[agent.y][agent.x] = (
            f"{agent.color}{agent.id}{RESET}"
        )
    for row in rendered_map:
        print(" ".join(row))
    print()


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

def shortest_path(start, target):
    start = tuple(start)
    target = tuple(target)

    def is_traversable(position):
        x, y = position
        return (
            0 <= y < len(MAP)
            and 0 <= x < len(MAP[y])
            and MAP[y][x] != "#"
        )

    if not is_traversable(start) or not is_traversable(target):
        return []

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heapq.heappush(open_set, (heuristic(start, target), start))

    came_from = {}

    g_score = {start: 0}
    f_score = {start: heuristic(start, target)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == target:
            path = []

            while current in came_from:
                path.append(current)
                current = came_from[current]

            path.append(start)
            path.reverse()

            return path

        x, y = current

        for neighbor in (
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ):
            if not is_traversable(neighbor):
                continue

            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                f = tentative_g + heuristic(neighbor, target)
                f_score[neighbor] = f

                heapq.heappush(open_set, (f, neighbor))

    return []

def print_route(route):
    rendered = [list(row) for row in MAP]

    for x, y in route:
        if rendered[y][x] == ".":
            rendered[y][x] = "*"

    for row in rendered:
        print(" ".join(row))
