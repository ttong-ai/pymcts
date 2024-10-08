import numpy as np
import time

from fastmcts.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from fastmcts.tree.search import MonteCarloTreeSearch
from fastmcts.games.tictactoe import TicTacToeGameState


def print_board(board):
    symbols = {0: " ", 1: "X", -1: "O"}
    print("\n" + "----" * len(board[0]) + "-")
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {symbols[cell]} |", end="")
        print("\n" + "----" * len(row) + "-")


def play_game(board_size: int = 3, connect: int = 3, simulations_per_move=100):
    initial_board_state = np.zeros((board_size, board_size), dtype=int)
    state = TicTacToeGameState(state=initial_board_state, next_to_move=0, win=connect)

    game_start_time = time.time()
    move_count = 0

    while not state.is_game_over():
        move_start_time = time.time()

        root = TwoPlayersGameMonteCarloTreeSearchNode(state=state)
        mcts = MonteCarloTreeSearch(root)
        best_node = mcts.best_action(simulations_per_move)

        state = best_node.state
        move_count += 1

        move_end_time = time.time()
        move_duration = move_end_time - move_start_time

        print(f"\nMove {move_count} (Player {'X' if state.next_to_move == -1 else 'O'}):")
        print(f"Action taken: {best_node.parent_action}")
        print(f"Simulations: {simulations_per_move}")
        print(f"Time taken: {move_duration:.2f} seconds")
        print_board(state.board)

    game_end_time = time.time()
    game_duration = game_end_time - game_start_time

    print("\nGame Over!")
    print(f"Total moves: {move_count}")
    print(f"Total game time: {game_duration:.2f} seconds")
    print(f"Winner: {'X' if state.game_result == 1 else 'O' if state.game_result == -1 else 'Draw'}")


if __name__ == "__main__":
    play_game(5, 4, simulations_per_move=10000)
