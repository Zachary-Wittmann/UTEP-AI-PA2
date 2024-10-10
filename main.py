import sys

# import random # Will be needed for Uniform Randomness

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


# Main function to run the simulation from the command line
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python <script> <input_file> <output_mode> <simulations>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_mode = sys.argv[2]
    simulations = int(sys.argv[3])

    algorithm, player, board = read_board_from_file(input_file)
    if algorithm == "UR":
        print(f"Uniform Random: {output_mode} with {simulations} simulations")
    elif algorithm == "PMCGS":
        print(
            f"Pure Monte Carlo Game Search: {output_mode} with {simulations} simulations"
        )
    elif algorithm == "UCT":
        print(
            f"Upper Confidence bound for Trees: {output_mode} with {simulations} simulations"
        )
    else:
        print(f"Unknown algorithm: {algorithm}")
        sys.exit(1)
    print("Board:")
    print_board(board)
