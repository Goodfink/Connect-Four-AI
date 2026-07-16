
EMPTY = 0
ROWS = 6
COLS = 7
P1 = 1
P2 = 2

directions = [
    (0, 1), # horizontal
    (1, 0), # vertical
    (1, 1), # diagonal down-right
    (1, -1) # diagonal down-left
]

def create_board():
    """
    Initializes an Empty Connect 4 board

    Board format:
    - 2D list of rows
    - 0 reps an empty cell
    - 1 represents player 1
    - 2 represents player 2
    - row 0 is the top of the board
    - the last row is the bottom of the board

    :return: An empty board
    """
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def legal_moves(board):
    """
    Returns a list of legal moves

    :param board: the current board state
    :return: List of legal columns which a move can be made in
    """
    legal_moves = []
    for col in range(COLS):
        if board[0][col] == EMPTY:
            legal_moves.append(col)

    return legal_moves

def apply_move(board, col, player):
    """
    Applies the given move to the given column

    :param board: the current board state
    :param col: the col which the move is applied too
    :param player: which player made the move
    :return: board state after applying move
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY and is_valid(row, col):
            board[row][col] = P1 if player == P1 else P2
            break

    return board

def is_draw(board):
    """
    Checks if the given board is a draw

    :param board: the current board state
    :return: True if the board is a draw, False otherwise
    """
    return is_winner(board) == EMPTY and len(legal_moves(board)) == 0

def is_terminal(board):
    """
    Checks if the game is over

    :param board: the current board state
    :return: True id the game is over, False otherwise
    """
    return is_winner(board) != EMPTY or is_draw(board)

def is_winner(board):
    """
    Checks if the given player is a winner in the current board state

    :param board: the current board state
    :return: Player token of the winner if there is a winner, Otherwise 0
    """
    for col in range(COLS):
        for row in range(ROWS - 1, -1 , -1):
            player = board[row][col]

            if player == EMPTY:
                continue

            for dr, dc in directions:
                in_a_row = 0

                for i in range(4):
                    r = row + dr * i
                    c = col + dc * i

                    if is_valid(r, c) and board[r][c] == player:
                        in_a_row += 1
                    else:
                        break

                if in_a_row == 4:
                    return player

    return EMPTY

def is_valid(row, col):
         return row >= 0 and row <= ROWS - 1 and col >= 0 and col <= COLS - 1

