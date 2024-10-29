import random
import math
import numpy as np
import matplotlib.pyplot as plt


# Constants
ROWS, COLS = 6, 7  # Board dimensions
WINNING_LENGTH = 4  # Connect Four win condition
RED = "R"  # Red player is the "Min" player
YELLOW = "Y"  # Yellow player is the "Max" player
EMPTY = "O"  # Empty space


# Utility Functions for Board
def create_board():
    """Create an empty board."""
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Display the current state of the board."""
    for row in board:
        print(" ".join(row))
    print()


def is_valid_move(board, col):
    """Check if a move is valid (i.e., the column is not full)."""
    return board[0][col] == EMPTY


def get_valid_moves(board):
    """Return a list of valid columns where a move can be made."""
    return [col for col in range(COLS) if is_valid_move(board, col)]


def drop_piece(board, row, col, piece):
    """Drop a piece into the board."""
    board[row][col] = piece


def get_next_open_row(board, col):
    """Get the next open row in the column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            return row


def check_win(board, piece):
    """Check for a win."""
    # Check horizontal locations for win
    for c in range(COLS - WINNING_LENGTH + 1):
        for r in range(ROWS):
            if all(board[r][c + i] == piece for i in range(WINNING_LENGTH)):
                return True

    # Check vertical locations for win
    for c in range(COLS):
        for r in range(ROWS - WINNING_LENGTH + 1):
            if all(board[r + i][c] == piece for i in range(WINNING_LENGTH)):
                return True

    # Check positively sloped diagonals
    for c in range(COLS - WINNING_LENGTH + 1):
        for r in range(ROWS - WINNING_LENGTH + 1):
            if all(board[r + i][c + i] == piece for i in range(WINNING_LENGTH)):
                return True

    # Check negatively sloped diagonals
    for c in range(COLS - WINNING_LENGTH + 1):
        for r in range(WINNING_LENGTH - 1, ROWS):
            if all(board[r - i][c + i] == piece for i in range(WINNING_LENGTH)):
                return True

    return False


def is_terminal_node(board):
    """Check if the board is a terminal node (win or draw)."""
    return (
        check_win(board, RED)
        or check_win(board, YELLOW)
        or len(get_valid_moves(board)) == 0
    )


def evaluate_board(board, piece):
    """Evaluate the board state."""
    if check_win(board, piece):
        return 1 if piece == YELLOW else -1
    return 0


# Algorithm 1: Uniform Random
def uniform_random(board, player, _=None):
    """Select a random valid move."""
    valid_moves = get_valid_moves(board)
    return random.choice(valid_moves)


# Algorithm 2: Pure Monte Carlo Game Search (PMCGS)
def pmcgs(board, player, num_simulations):
    """Run Pure Monte Carlo Search."""
    valid_moves = get_valid_moves(board)
    move_scores = {col: 0 for col in valid_moves}

    for col in valid_moves:
        for _ in range(num_simulations):
            temp_board = [row[:] for row in board]  # Copy the board
            row = get_next_open_row(temp_board, col)
            drop_piece(temp_board, row, col, player)
            winner = run_simulation(temp_board, switch_player(player))
            move_scores[col] += winner

    # Select the move with the highest score
    best_move = max(move_scores, key=move_scores.get)
    return best_move


def run_simulation(board, player):
    """Run a random simulation from the current board state."""
    current_player = player
    while not is_terminal_node(board):
        valid_moves = get_valid_moves(board)
        col = random.choice(valid_moves)
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, current_player)
        current_player = switch_player(current_player)

    if check_win(board, YELLOW):
        return 1
    elif check_win(board, RED):
        return -1
    return 0


# Updated best move selection in UCT
def uct(board, player, num_simulations, exploration=1.41):
    """Run UCT algorithm."""
    valid_moves = get_valid_moves(board)
    move_stats = {
        col: {"wins": 0, "plays": 1} for col in valid_moves
    }  # Initialize plays with 1

    for _ in range(num_simulations):
        col = select_move_uct(move_stats, valid_moves, exploration)
        temp_board = [row[:] for row in board]
        row = get_next_open_row(temp_board, col)
        drop_piece(temp_board, row, col, player)
        winner = run_simulation(temp_board, switch_player(player))
        update_stats(move_stats, col, winner)

    # Filter out moves with zero plays before calculating best move
    best_move = max(
        (col for col in valid_moves if move_stats[col]["plays"] > 0),
        key=lambda col: move_stats[col]["wins"] / move_stats[col]["plays"],
    )
    return best_move


def select_move_uct(move_stats, valid_moves, exploration):
    """Select a move using UCB."""
    total_plays = sum(move_stats[col]["plays"] for col in valid_moves)
    ucb_values = {}

    for col in valid_moves:
        wins, plays = move_stats[col]["wins"], move_stats[col]["plays"]
        if plays == 0:
            ucb_values[col] = float("inf")  # Force exploration of this move
        else:
            avg_win = wins / plays
            ucb_values[col] = avg_win + exploration * math.sqrt(
                math.log(total_plays) / plays
            )

    return max(ucb_values, key=ucb_values.get)


def update_stats(move_stats, col, result):
    """Update win/play statistics after a simulation."""
    move_stats[col]["plays"] += 1
    move_stats[col]["wins"] += result


def switch_player(player):
    """Switch the current player."""
    return YELLOW if player == RED else RED


# Running the tournament
def play_game(
    algorithm1, algorithm2, num_simulations1, num_simulations2, verbose=False
):
    board = create_board()
    current_player = RED  # Start with Red
    algorithms = {RED: algorithm1, YELLOW: algorithm2}

    while not is_terminal_node(board):
        if verbose:
            print_board(board)
        valid_moves = get_valid_moves(board)
        if current_player == RED:
            move = algorithm1(board, RED, num_simulations1)
        else:
            move = algorithm2(board, YELLOW, num_simulations2)

        row = get_next_open_row(board, move)
        drop_piece(board, row, move, current_player)
        if check_win(board, current_player):
            return 1 if current_player == YELLOW else -1
        current_player = switch_player(current_player)

    return 0  # Draw


def run_tournament():
    algorithms = [
        ("UR", uniform_random, 0),
        ("PMCGS (500)", pmcgs, 5),
        ("PMCGS (10000)", pmcgs, 100),
        ("UCT (500)", uct, 5),
        ("UCT (10000)", uct, 100),
    ]

    results = np.zeros((len(algorithms), len(algorithms)))

    for i, (name1, algo1, sims1) in enumerate(algorithms):
        for j, (name2, algo2, sims2) in enumerate(algorithms):
            if i != j:
                for _ in range(100):  # Play 100 games
                    result = play_game(algo1, algo2, sims1, sims2, verbose=False)
                    if result == 1:
                        results[i][j] += 1  # Algo1 wins
                    elif result == -1:
                        results[j][i] += 1  # Algo2 wins

    # Display results as a heatmap
    fig, ax = plt.subplots()
    cax = ax.matshow(results, cmap="Blues")

    # Add color bar
    plt.colorbar(cax)

    # Set up axes
    ax.set_xticks(np.arange(len(algorithms)))
    ax.set_yticks(np.arange(len(algorithms)))
    ax.set_xticklabels([name for name, _, _ in algorithms], rotation=45, ha="right")
    ax.set_yticklabels([name for name, _, _ in algorithms])

    # Add labels
    plt.xlabel("Opponent Algorithm")
    plt.ylabel("Player Algorithm")
    plt.title("Tournament Results (%)")

    # Annotate the heatmap with percentage values
    for (i, j), value in np.ndenumerate(results):
        if i != j:  # Skip diagonal
            ax.text(j, i, f"{value:.1f}%", ha="center", va="center", color="black")

    plt.show()


if __name__ == "__main__":
    run_tournament()
