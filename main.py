import sys
import random


class Node:
    def __init__(self, move, wi, ni):
        self.move = move
        self.wi = wi
        self.ni = ni


# Constants
ROWS = 6
COLUMNS = 7
RED = "R"  # Min player
YELLOW = "Y"  # Max player
EMPTY = "O"


# Helper function to read the board from the file
def read_board_from_file(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    algorithm = lines[0].strip()
    player = lines[1].strip()
    board = [list(line.strip()) for line in lines[2:]]
    return algorithm, player, board


# Helper function to print the board
def print_board(board):
    for row in board:
        print(" ".join(row))
    print()


# Helper function to check valid moves
def valid_moves(board):
    return [c for c in range(COLUMNS) if board[0][c] == EMPTY]


# Helper function creates a list of the seven possible legal moves for the board
# def create_valid_moves(board):
#     valid_movs = []
#     found_col = []
#     for row in range(ROWS - 1, -1, -1):
#         for col in range(COLUMNS - 1, -1, -1):
#             if board[row][col] == EMPTY and col not in found_col:
#                 valid_movs.append([row, col])
#                 found_col.append(col)
#                 pass
#     return valid_movs


# Helper function to make a move
def make_move(board, column, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == EMPTY:
            board[row][column] = player
            return row, column


# Helper function to make a move, updates board and updates legal moves
# def make_move(board, moves, player):
#     selected = random.choice(moves)
#     board[selected[0]][selected[1]] = player
#     if (
#         selected[0] == 0
#     ):  # if rows == 0 then there are no more legal moves for that board column
#         moves.remove(selected)
#     else:
#         pos = moves.index(selected)
#         moves[pos][
#             0
#         ] -= 1  # updates the board row as new legal move, column stays the same
#     return (
#         moves,
#         selected[1],
#     )  # returns updated legal moves and the column of the selected move


def check_winner(board, last_move):
    row, col = last_move
    player = board[row][col]

    # Direction vectors for (dx, dy) moves: horizontal, vertical, and two diagonals
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    def count_in_direction(dx, dy):
        """Counts consecutive pieces in a given direction (dx, dy) starting from (row, col)."""
        count = 0
        r, c = row, col
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player:
            count += 1
            r += dx
            c += dy
        return count

    for dx, dy in directions:
        # Count pieces in both directions from the last move (including the last move itself)
        total_count = count_in_direction(dx, dy) + count_in_direction(-dx, -dy) - 1
        if total_count >= 4:
            return 1 if player == YELLOW else -1

    # Check for draw (no more valid moves)
    if not valid_moves(board):
        return 0  # Draw

    # No winner or draw yet
    return None


# Simulate a random rollout (helper function for PMC/UCT)
def random_rollout(board, player):
    current_player = player
    while True:
        if not valid_moves(board):
            return 0  # Draw
        move = random.choice(valid_moves(board))
        row, col = make_move(
            board, move, current_player
        )  # Ensure both row and column are returned

        winner = check_winner(board, (row, col))  # Correctly pass the row, col pair
        if winner is not None:
            return winner
        current_player = RED if current_player == YELLOW else YELLOW


# Algorithm 1: Uniform Random (UR)
def uniform_random(board, player, output):

    moves = valid_moves(board)

    if not moves:
        print("No valid moves available.")
        return None

    if output == "Verbose":
        print("Initial board:")
        print_board(board)

    moves, selected_move = make_move(board, moves, player)

    print(f"FINAL Move selected: {selected_move + 1}")

    if output != "None":
        print("Final board state:")
        print_board(board)


# Algorithm 2: Pure Monte Carlo Game Search (PMCGS)
def pmcgs(board, player, simulations, output="None"):
    # wi and ni track the number of wins and the number of simulations for each column
    wi = [0] * COLUMNS  # Wins for each column
    ni = [0] * COLUMNS  # Number of simulations for each column

    for sim in range(simulations):
        if output == "Verbose":
            print(f"Simulation {sim + 1}")

        for col in range(COLUMNS):
            if board[0][col] != EMPTY:  # Skip full columns (invalid moves)
                if output == "Verbose":
                    print(f"Column {col + 1}: Null (full column)")
                continue

            # Make a temporary board copy and perform a move for the player
            temp_board = [row[:] for row in board]  # Copy the board
            make_move(temp_board, col, player)  # Only integer `col` is used here

            # Perform a random rollout starting from the current board state
            result = random_rollout(
                temp_board, player
            )  # Pass the player token as string

            # Update wi and ni for this column
            ni[col] += 1
            wi[col] += result

            if output == "Verbose":
                print(f"wi: {wi[col]}\nni: {ni[col]}\nMove selected: {col + 1}\n")

        if output == "Verbose":
            print("NODE ADDED\n")  # Indicate a node addition

    # Print the final values for each column (wi/ni) or 'Null' for invalid moves
    if output == "Verbose":
        for col in range(COLUMNS):
            if ni[col] == 0:  # No simulations for this column, means it's a full column
                print(f"Column {col + 1}: Null")
            else:
                value = wi[col] / ni[col]
                print(f"Column {col + 1}: {value:.2f}")

    # Select the column with the best wi/ni value (ignoring full columns)
    best_move = max(
        range(COLUMNS), key=lambda c: (wi[c] / ni[c]) if ni[c] > 0 else float("-inf")
    )

    print(f"FINAL Move selected: {best_move + 1}")
    return best_move


# Algorithm 3: Upper Confidence Bound for Trees (UCT)
def uct(board, player, simulations, output):
    pass


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python <script> <input_file> <output_mode> <simulations>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_mode = sys.argv[2]
    simulations = int(sys.argv[3])

    algorithm, player, board = read_board_from_file(input_file)
    if algorithm == "UR":
        uniform_random(
            board, player, output_mode
        )  # ignores simulations due to the number not mattering for Uniform Random
    elif algorithm == "PMCGS":
        pmcgs(board, player, simulations, output_mode)
    elif algorithm == "UCT":
        print(
            f"Upper Confidence bound for Trees: {output_mode} with {simulations} simulations"
        )
        print("Board:")
        print_board(board)
    else:
        print(f"Unknown algorithm: {algorithm}")
        sys.exit(1)
