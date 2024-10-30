def tournament(board, players, output):
    playerWins = 0
    player2Wins = 0
    draws = 0
    # keeps track of the player combinations seen
    seen = []
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
                if winner == player:
                    playerWins += 1
                elif winner == player2:
                    player2Wins += 1
                else:
                    draws += 1
            print(
                player
                + " had "
                + str(playerWins)
                + " wins against "
                + player2
                + " who had "
                + str(player2Wins)
                + " wins"
            )
            print("There were " + str(draws) + " draws")
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
            move = pmcgs(board, color, 500, output)
        elif curr == "PMCGS(10000)":
            move = pmcgs(board, color, 10000, output)
        elif curr == "UCT(500)":
            move = uct(board, color, 500, output)
        elif curr == "UCT(10000)":
            move = uct(board, color, 10000, output)

        if move is None:
            print("No valid moves left. Draw.")
            return 0  # Indicate a draw

        result = make_move(board, move, color)  # This now should return (row, col) or None
        if result is None:
            print("Invalid move; column is full.")
            return 0  # Indicate a draw

        row, col = result
        winner = check_winner(board, (row, col))

        if winner is not None:
            return winner

        curr = player2 if curr == player else player
        color = YELLOW if color == RED else RED