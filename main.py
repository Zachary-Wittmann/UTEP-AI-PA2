import sys
import random

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
#def valid_moves(board):
#    return [c for c in range(COLUMNS) if board[0][c] == EMPTY]
#Helper function creates a list of the seven possible legal moves for the board
def create_valid_moves(board):
    valid_movs = []
    found_col = []
    for row in range(ROWS-1,-1,-1):
        for col in range(COLUMNS-1,-1,-1):
            if (board[row][col] == EMPTY and col not in found_col):
                valid_movs.append([row,col])
                found_col.append(col)
                pass
    return valid_movs

# Helper function to make a move
#def make_move(board, column, player):
#    for row in range(ROWS - 1, -1, -1):
#        if board[row][column] == EMPTY:
#            board[row][column] = player
#            return row, column
#Helper function to make a move, updates board and updates legal moves
def make_move(board, moves, player):
    selected = random.choice(moves)
    board[selected[0]][selected[1]] = player
    if(selected[0] == 0): #if rows == 0 then there are no more legal moves for that board column
        moves.remove(selected)
    else:
        pos = moves.index(selected)
        moves[pos][0]-=1 #updates the board row as new legal move, column stays the same
    return moves, selected[1] #returns updated legal moves and the column of the selected move


# Algorithm 1: Uniform Random (UR)
def uniform_random(board, player, output):

    moves = create_valid_moves(board)

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
        print(
            f"Pure Monte Carlo Game Search: {output_mode} with {simulations} simulations"
        )
        print("Board:")
        print_board(board)
    elif algorithm == "UCT":
        print(
            f"Upper Confidence bound for Trees: {output_mode} with {simulations} simulations"
        )
        print("Board:")
        print_board(board)
    else:
        print(f"Unknown algorithm: {algorithm}")
        sys.exit(1)
