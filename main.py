import random
from typing import Optional

from agent import Agent, AgentState, create_agents
from map import shortest_path
from task import Task, create_task


AUCTION_MANAGER = "DispatchManager"


def calculate_bid_cost(agent: Agent, task: Task) -> Optional[int]:
    """Return the travel cost for an agent to collect and deliver a task."""
    to_depot = shortest_path((agent.x, agent.y), (task.depot_x, task.depot_y))
    to_destination = shortest_path(
        (task.depot_x, task.depot_y),
        (task.dest_x, task.dest_y),
    )

    if not to_depot or not to_destination:
        return None

    # A path contains both end points, so its number of travelled cells is n - 1.
    return len(to_depot) - 1 + len(to_destination) - 1


def determine_winner(agents: list[Agent], task: Task) -> Optional[tuple[Agent, int]]:
    bids = [
        (agent, cost)
        for agent in agents
        if agent.state == AgentState.IDLE
        if (cost := calculate_bid_cost(agent, task)) is not None
    ]

    if not bids:
        return None

    # Agent ID makes equal bids deterministic.
    return min(bids, key=lambda bid: (bid[1], bid[0].id))


def perform_bidding(
    agents: list[Agent], tasks: list[Task], round_number: int
) -> list[dict[str, object]]:
    """Run an auction and log the required result data for every task."""
    auction_records: list[dict[str, object]] = []

    for task in tasks:
        if task.agent_id is not None:
            continue

        available_bidders = [agent for agent in agents if agent.state == AgentState.IDLE]
        winning_bid = determine_winner(agents, task)

        if winning_bid is None:
            record = {
                "round": round_number,
                "task": task.id,
                "manager": AUCTION_MANAGER,
                "bidders": len(available_bidders),
                "winner": "none",
                "cost": "none",
            }
        else:
            winner, cost = winning_bid
            task.agent_id = winner.id
            winner.assign_task(task)
            record = {
                "round": round_number,
                "task": task.id,
                "manager": AUCTION_MANAGER,
                "bidders": len(available_bidders),
                "winner": f"Agent {winner.id}",
                "cost": cost,
            }

        auction_records.append(record)
        print(
            "AUKTIONSERGEBNIS "
            f"Runde={record['round']}, Auftrag={record['task']}, "
            f"Manager={record['manager']}, Bieter={record['bidders']}, "
            f"Gewinner={record['winner']}, GeboteneKosten={record['cost']}"
        )

    return auction_records


def run_until_delivered(agents: list[Agent], task: Task) -> None:
    """Advance the simulation until the auction winner has delivered the task."""
    winner = next(agent for agent in agents if agent.id == task.agent_id)
    while winner.task is task:
        for agent in agents:
            agent.update()


def main() -> None:
    # A fixed seed makes the submitted result evidence reproducible.
    random.seed(42)
    agents = create_agents(n=2)

    for round_number in range(1, 6):
        task = create_task(round_number - 1)
        perform_bidding(agents, [task], round_number)

        # Starting the next round only after delivery means each round has a
        # meaningful set of free bidders.
        run_until_delivered(agents, task)


if __name__ == "__main__":
    main()
