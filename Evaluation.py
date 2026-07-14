import random

from gameEngine import create_board, apply_move, is_terminal, is_winner, P1, P2
from agents import RandomAgent, RuleBasedAgent, MinimaxAgent, timed_move

random.seed(42)


def play_game(agent1, agent2):
    board = create_board()

    player = P1

    time1 = 0
    time2 = 0

    moves1 = 0
    moves2 = 0

    while not is_terminal(board):

        if player == P1:
            move, t = timed_move(agent1, board, P1)
            time1 += t
            moves1 += 1
        else:
            move, t = timed_move(agent2, board, P2)
            time2 += t
            moves2 += 1

        apply_move(board, move, player)

        player = P2 if player == P1 else P1

    return (
        is_winner(board),
        time1 / moves1,
        time2 / moves2
    )


def run_match(agent1, name1, agent2, name2):

    wins1 = 0
    wins2 = 0
    draws = 0

    times1 = []
    times2 = []

    for i in range(30):

        # Swap who starts after 15 games
        if i < 15:
            winner, t1, t2 = play_game(agent1, agent2)

            if winner == P1:
                wins1 += 1
            elif winner == P2:
                wins2 += 1
            else:
                draws += 1

        else:
            winner, t2, t1 = play_game(agent2, agent1)

            if winner == P1:
                wins2 += 1
            elif winner == P2:
                wins1 += 1
            else:
                draws += 1

        times1.append(t1)
        times2.append(t2)

    print(f"\n{name1} vs {name2}")
    print(f"{name1} wins: {wins1}")
    print(f"{name2} wins: {wins2}")
    print(f"Draws: {draws}")
    print(f"{name1} avg time: {sum(times1)/30:.6f} sec")
    print(f"{name2} avg time: {sum(times2)/30:.6f} sec")


random_agent = RandomAgent()
rule_agent = RuleBasedAgent()
minimax_agent = MinimaxAgent(depth=4)

run_match(random_agent, "Random", rule_agent, "Rule-Based")
run_match(rule_agent, "Rule-Based", minimax_agent, "Minimax")
run_match(minimax_agent, "Minimax", random_agent, "Random")

print("\nRandom seed: 42")
