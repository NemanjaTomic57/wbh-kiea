from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import random


CUSTOM_MAP = (
    "####################",
    "#D....#.......Z....#",
    "#.###.#.#####.###..#",
    "#.....#.....#......#",
    "#.#####.###.#.###..#",
    "#.......#...#......#",
    "#.#####.#.#####.##.#",
    "#..Z....#.....#....#",
    "#.###.#####.#.###..#",
    "#....#.....#....D..#",
    "#.##.#.###.#####...#",
    "#......Z...........#",
    "####################",
)


class AgentType(Enum):
    STANDARD = "Standard"
    EXPRESS = "Express"


class ActionType(Enum):
    MOVE = "move"
    PICK_UP = "pick_up"
    DELIVER = "deliver"
    SEND_MESSAGE = "send_message"
    WAIT = "wait"


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def neighbors(self) -> list["Position"]:
        return [
            Position(self.x, self.y - 1),
            Position(self.x + 1, self.y),
            Position(self.x, self.y + 1),
            Position(self.x - 1, self.y),
        ]


@dataclass
class Message:
    sender_id: int
    recipient_id: int
    text: str


@dataclass
class Agent:
    agent_id: int
    agent_type: AgentType
    position: Position
    speed: int
    capacity: int
    battery: int
    cargo: int = 0
    delivered: int = 0
    inbox: list[Message] = field(default_factory=list)

    @classmethod
    def standard(cls, agent_id: int, position: Position) -> "Agent":
        return cls(
            agent_id=agent_id,
            agent_type=AgentType.STANDARD,
            position=position,
            speed=1,
            capacity=2,
            battery=20,
        )

    @classmethod
    def express(cls, agent_id: int, position: Position) -> "Agent":
        return cls(
            agent_id=agent_id,
            agent_type=AgentType.EXPRESS,
            position=position,
            speed=2,
            capacity=1,
            battery=14,
        )

    def read_messages(self) -> list[str]:
        texts = [
            f"A{self.agent_id} liest Nachricht von A{message.sender_id}: {message.text}"
            for message in self.inbox
        ]
        self.inbox.clear()
        return texts


@dataclass(frozen=True)
class Action:
    action_type: ActionType
    recipient_id: int | None = None
    text: str = ""


class CityMap:
    def __init__(self, rows: tuple[str, ...]) -> None:
        if len(rows) < 10 or any(len(row) < 10 for row in rows):
            raise ValueError("Die Karte muss mindestens 10 x 10 Zellen haben.")
        if len({len(row) for row in rows}) != 1:
            raise ValueError("Alle Kartenzeilen muessen gleich lang sein.")

        self.rows = rows
        self.height = len(rows)
        self.width = len(rows[0])
        self.depots = self._find_cells("D")
        self.destinations = self._find_cells("Z")

        if len(self.depots) < 2:
            raise ValueError("Die Karte muss mindestens zwei Depots enthalten.")
        if len(self.destinations) < 3:
            raise ValueError("Die Karte muss mindestens drei Lieferziele enthalten.")

    def _find_cells(self, cell_type: str) -> list[Position]:
        positions: list[Position] = []
        for y, row in enumerate(self.rows):
            for x, cell in enumerate(row):
                if cell == cell_type:
                    positions.append(Position(x, y))
        return positions

    def is_inside(self, position: Position) -> bool:
        return 0 <= position.x < self.width and 0 <= position.y < self.height

    def is_obstacle(self, position: Position) -> bool:
        return self.rows[position.y][position.x] == "#"

    def is_driveable(self, position: Position) -> bool:
        return self.is_inside(position) and not self.is_obstacle(position)

    def is_depot(self, position: Position) -> bool:
        return position in self.depots

    def is_destination(self, position: Position) -> bool:
        return position in self.destinations

    def free_cells(self) -> list[Position]:
        cells: list[Position] = []
        for y, row in enumerate(self.rows):
            for x, cell in enumerate(row):
                position = Position(x, y)
                if cell != "#":
                    cells.append(position)
        return cells

    def render(self, agents: list[Agent]) -> str:
        rendered = [list(row) for row in self.rows]
        for agent in agents:
            rendered[agent.position.y][agent.position.x] = str(agent.agent_id)
        return "\n".join("".join(row) for row in rendered)


class Simulation:
    def __init__(self, city_map: CityMap, seed: int = 7) -> None:
        self.city_map = city_map
        self.random = random.Random(seed)
        self.agents = self._create_agents()
        self.pending_messages: list[Message] = []
        self.step_number = 0

    def _create_agents(self) -> list[Agent]:
        starts = self.random.sample(self.city_map.free_cells(), 4)
        return [
            Agent.standard(1, starts[0]),
            Agent.standard(2, starts[1]),
            Agent.express(3, starts[2]),
            Agent.express(4, starts[3]),
        ]

    def run(self, steps: int) -> None:
        print("Besonderheit der Karte:")
        print(
            "Die eigene Karte ist groesser als 10 x 10 und kombiniert zwei Depots, "
            "drei Lieferziele, Engstellen, Sackgassen und alternative Routen. "
            "Dadurch koennen Agenten einander blockieren, ohne dass Ziele "
            "grundsaetzlich unerreichbar sind."
        )
        print("\nKarte direkt nach Initialisierung und Agentenplatzierung:")
        print(self.city_map.render(self.agents))
        self._print_agent_state()

        for _ in range(steps):
            self.step()

        print(f"\nKarte nach {steps} Simulationsschritten:")
        print(self.city_map.render(self.agents))
        self._print_agent_state()

    def step(self) -> None:
        self.step_number += 1
        self._deliver_pending_messages()

        occupied = {agent.position: agent.agent_id for agent in self.agents}
        for agent in self.agents:
            for line in agent.read_messages():
                print(f"Schritt {self.step_number}: {line}")

            action = self._plan_action(agent)
            self._execute_action(agent, action, occupied)

    def _deliver_pending_messages(self) -> None:
        agents_by_id = {agent.agent_id: agent for agent in self.agents}
        for message in self.pending_messages:
            agents_by_id[message.recipient_id].inbox.append(message)
        self.pending_messages.clear()

    def _plan_action(self, agent: Agent) -> Action:
        if self.city_map.is_destination(agent.position) and agent.cargo > 0:
            return Action(ActionType.DELIVER)
        if self.city_map.is_depot(agent.position) and agent.cargo < agent.capacity:
            return Action(ActionType.PICK_UP)
        if self.step_number % 3 == 0:
            possible_recipients = [
                other.agent_id for other in self.agents if other.agent_id != agent.agent_id
            ]
            recipient_id = self.random.choice(possible_recipients)
            return Action(
                ActionType.SEND_MESSAGE,
                recipient_id=recipient_id,
                text=f"Status von A{agent.agent_id}: Position {agent.position}",
            )
        if agent.battery <= 0:
            return Action(ActionType.WAIT)
        return Action(ActionType.MOVE)

    def _execute_action(
        self,
        agent: Agent,
        action: Action,
        occupied: dict[Position, int],
    ) -> None:
        if action.action_type == ActionType.PICK_UP:
            agent.cargo += 1
            print(f"Schritt {self.step_number}: A{agent.agent_id} nimmt ein Paket auf.")
            return

        if action.action_type == ActionType.DELIVER:
            agent.cargo -= 1
            agent.delivered += 1
            print(f"Schritt {self.step_number}: A{agent.agent_id} liefert ein Paket ab.")
            return

        if action.action_type == ActionType.SEND_MESSAGE and action.recipient_id is not None:
            self.pending_messages.append(
                Message(agent.agent_id, action.recipient_id, action.text)
            )
            print(
                f"Schritt {self.step_number}: A{agent.agent_id} sendet eine Nachricht "
                f"an A{action.recipient_id}."
            )
            return

        if action.action_type == ActionType.MOVE:
            self._move_agent(agent, occupied)
            return

        print(f"Schritt {self.step_number}: A{agent.agent_id} wartet.")

    def _move_agent(self, agent: Agent, occupied: dict[Position, int]) -> None:
        for _ in range(agent.speed):
            candidates = [
                position
                for position in agent.position.neighbors()
                if self.city_map.is_driveable(position)
                and position not in occupied
            ]
            if not candidates or agent.battery <= 0:
                print(f"Schritt {self.step_number}: A{agent.agent_id} bleibt stehen.")
                return

            old_position = agent.position
            new_position = self.random.choice(candidates)
            del occupied[old_position]
            occupied[new_position] = agent.agent_id
            agent.position = new_position
            agent.battery -= 1
            print(
                f"Schritt {self.step_number}: A{agent.agent_id} faehrt "
                f"von {old_position} nach {new_position}."
            )

    def _print_agent_state(self) -> None:
        print("\nAgentenstatus:")
        for agent in self.agents:
            print(
                f"A{agent.agent_id}: Typ={agent.agent_type.value}, "
                f"Position={agent.position}, Geschwindigkeit={agent.speed}, "
                f"Kapazitaet={agent.capacity}, Ladung={agent.cargo}, "
                f"Batterie={agent.battery}, Ausgeliefert={agent.delivered}"
            )


def main() -> None:
    city_map = CityMap(CUSTOM_MAP)
    simulation = Simulation(city_map)
    simulation.run(steps=5)


if __name__ == "__main__":
    main()
