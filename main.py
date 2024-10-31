import sys
import random
import math


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


# Helper function to make a move
def make_move(board, column, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == EMPTY:
            board[row][column] = player
            return row, column


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

def uct_rollout(board, player, wi, ni, parent):
    current_player = player
    while True:
        # print("hi")
        if not valid_moves(board):
            return 0  # Draw
        move = (
            ((wi[parent]) / ni[parent])
            + math.sqrt(2) * math.sqrt(math.log(parent / ni[parent]))
            if ni[parent] > 0
            else random.choice(valid_moves(board))
        )
        # max(
        # range(COLUMNS), key=lambda c: ((wi[c] / ni[c]) + math.sqrt(2) * math.sqrt(math.log(parent)/ni[c])) if ni[c] > 0 else random.choice(valid_moves(board))
        # )
        row, col = make_move(board, move, current_player)

        winner = check_winner(board, (row, col))
        if winner is not None:
            return winner
        current_player = RED if current_player == YELLOW else YELLOW

def check_move_score(board, move):
    row, col = move
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

    return total_count

# heuristic to prioritize moves based on more likely to win states
def priority_rollout(board, player):
    current_player = player
    best_move = 0
    best_score = float('-inf')
    while True:
        if not valid_moves(board):
           return 0 #Draw
        for move in valid_moves(board):
            temp_board = [row[:] for row in board]
            row, col = make_move(temp_board, move, current_player)
            score = check_move_score(temp_board, (row, col))
            if score < best_score:
                best_score = score
                best_move = move
            else:
                best_move = random.choice(valid_moves(board))
        last_row, last_col = make_move(board, best_move, current_player)
        winner = check_winner(board, (last_row, last_col))
        if winner is not None:
            return winner
        current_player = RED if current_player == YELLOW else YELLOW



# Algorithm 1: Uniform Random (UR)
def uniform_random(board, player, output):

    moves = valid_moves(board)

    if not moves:
        print("No valid moves available.")
        return None

    selected_move = random.choice(moves)

    if output == "Verbose":
        print("Initial board:")
        print_board(board)

    make_move(board, selected_move, player)

    print(f"FINAL Move selected: {selected_move + 1}")

    if output != "None":
        print("Final board state:")
        print_board(board)
    return selected_move


# Algorithm 2: Pure Monte Carlo Game Search (PMCGS)
def pmcgs(board, player, simulations, output):
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
    if output == "Verbose" or output == "Brief":
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
    # wi and ni track the number of wins and the number of simulations for each column
    wi = [0] * COLUMNS  # Wins for each column
    ni = [0] * COLUMNS  # Number of simulations for each column

    for sim in range(simulations):
        if output == "Verbose":
            print(f"Simulation {sim + 1}")

        for col in valid_moves(board):
            new_board = [row[:] for row in board]
            make_move(new_board, col, player)
            result = random_rollout(new_board, player)
            ni[col] += 1
            wi[col] += result
            if output == "Verbose":
                print(f"wi: {wi[col]}\nni: {ni[col]}\nMove selected: {col + 1}\n")

        # UCB values calculations
        ucb_values = [
            (
                wi[i] / ni[i] + math.sqrt(2 * math.log(sim + 1) / ni[i])
                if ni[i] > 0
                else float("inf")
            )
            for i in range(COLUMNS)
        ]
        selected_move = ucb_values.index(max(ucb_values))
        if output == "Verbose":
            print("NODE ADDED\n")

    if output == "Verbose" or output == "Brief":
        for col, ucb in enumerate(ucb_values):
            print(f"Column {col + 1}: {ucb}")
    
    print(f"FINAL Move selected: {selected_move + 1}")
    return selected_move

def player_helper(board, move, player):
    row, col = make_move(board, move, player)
    win_check = check_winner(board, (row, col))
    return board, win_check


def play_human_player(board):
    winner = False
    print("Human player: R, Computer player: Y")
    while True:
        moves = valid_moves(board)
        if not valid_moves(board):
            print("Draw")
            break
        print("Current Board:")
        print_board(board)
        #human player move
        player_move = int(input("Enter a move(1-7): "))
        while player_move-1 not in moves:
            print("Illegal move chosen")
            player_move = int(input("Enter a move(1-7): "))
        board, winner = player_helper(board, player_move-1, RED)
        #check if human player has made winning move
        if winner:
            print_board(board)
            print("RED WINS")
            break
        #start of computer move
        moves = valid_moves(board)
        if not valid_moves(board):
            print("Draw")
            break
        print("Computer is thinking...")
        computer_move = pmcgs(board, YELLOW, 100, "None") #uses uct to decide the computer move
        print(f"Computer chose move: {computer_move+1}")
        board, winner = player_helper(board, computer_move, YELLOW)
        #check if computer player has made winning move
        if winner:
            print_board(board)
            print("YELLOW WINS")
            break

def tournament(board, players, output):
    playerWins = 0
    player2Wins = 0
    draws = 0
    # keeps track of the player combinations seen
    seen = []
    with open("tournament_results_easy.txt", "w") as result_file:
        for player in players:
            for player2 in players:
                if seen.count(player + player2) > 0:
                    continue
                if seen.count(player2 + player) > 0:
                    continue
                seen.append(player + player2)
                seen.append(player2 + player)
                for sim in range(100):
                    curr_board = [row[:] for row in board]
                    winner = play(curr_board, player, player2, simulations, output)
                    if winner == 1:
                        playerWins += 1
                    elif winner == -1:
                        player2Wins += 1
                    else:
                        draws += 1
                result_file.write(
                    f"{player} had {playerWins} wins against {player2} who had {player2Wins} wins\n"
                )
                result_file.write(f"There were {draws} draws\n")
                playerWins = 0
                player2Wins = 0
                draws = 0


def play(board, player, player2, simulations, output):
    curr = player
    color = RED
    while True:
        if curr == "UR":
            move = uniform_random(board, color, output)
        elif curr == "PMCGS(500)":
            move = pmcgs(board, color, 5, output)
        elif curr == "PMCGS(10000)":
            move = pmcgs(board, color, 100, output)
        elif curr == "UCT(500)":
            move = uct(board, color, 5, output)
        elif curr == "UCT(10000)":
            move = uct(board, color, 100, output)

        if move is None:
            print("Draw")
            return 0  

        result = make_move(board, move, color)  
        if result is None:
            print("Invalid move")
            return 0

        row, col = result
        winner = check_winner(board, (row, col))

        if winner is not None:
            return winner

        curr = player2 if curr == player else player
        color = YELLOW if color == RED else RED


if __name__ == "__main__":
    tournament_experiment_mode = False

    if len(sys.argv) != 4:
        if len(sys.argv) == 5:
            tournament_experiment_mode = True
        else:    
            print("Usage: python <script> <input_file> <output_mode> <simulations>")
            sys.exit(1)

    input_file = sys.argv[1]
    output_mode = sys.argv[2]
    simulations = int(sys.argv[3])

    algorithm, player, board = read_board_from_file(input_file)

    if tournament_experiment_mode:
        print("Round Robin Tournament")
        players = ["UR", "PMCGS(500)", "PMCGS(10000)", "UCT(500)", "UCT(10000)"]
        tournament(board, players, "None")
        sys.exit(1)

    if algorithm == "UR":
        uniform_random(
            board, player, output_mode
        )  # ignores simulations due to the number not mattering for Uniform Random
    elif algorithm == "PMCGS":
        pmcgs(board, player, simulations, output_mode)
    elif algorithm == "UCT":
        uct(board, player, simulations, output_mode)
    elif algorithm == "HUMAN":
        play_human_player(board)
        #ignores the player, simulations and output_mode. starts with an empty board
    else:
        print(f"Unknown algorithm: {algorithm}")
        sys.exit(1)