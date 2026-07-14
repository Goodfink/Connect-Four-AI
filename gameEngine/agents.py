import random, math, time, copy
from gameEngine import (
    legal_moves,
    apply_move,
    is_terminal,
    is_winner,
    is_draw,
    directions,
    is_valid,
    COLS,
    ROWS,
    EMPTY,
    P1,
    P2,
)
# Helper functions
def get_opponent(player):
    """Returns the other player's token."""
    return P2 if player == P1 else P1
 
 
def simulate_move(board, col, player):
    """
    Returns a NEW board with player's move applied to col, leaving the
    original board untouched. Agents use this instead of apply_move
    directly so that look-ahead never mutates the real game state.
    """
    board_copy = copy.deepcopy(board)
    return apply_move(board_copy, col, player)
 
 
def get_drop_row(board, col):
    """Returns the row a disc would land on if dropped in col right now."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            return row
    return None
 
 
def find_winning_moves(board, player):
    """Returns every legal move that would immediately win for player"""
    winning = []
    for col in legal_moves(board):
        test_board = simulate_move(board, col, player)
        if is_winner(test_board) == player:
            winning.append(col)
    return winning
 
 
def timed_move(agent, board, player):
    """
    Wraps any agent's get_move call and returns (move, elapsed_seconds)
    Useful for Requirement 3's "average decision time per move" metric
    """
    start = time.perf_counter()
    move = agent.get_move(board, player)
    elapsed = time.perf_counter() - start
    return move, elapsed



# Agent 1: Random
class RandomAgent:
    def get_move(self, board, player):
        return random.choice(legal_moves(board))

    


# Agent 2: Rule-based
# Manually defined and prioritized rules
class RuleBasedAgent:
    def get_move(self, board, player):
        opponent = get_opponent(player)
        moves = legal_moves(board)
 
        # Rule 1: win immediately.
        winning = find_winning_moves(board, player)
        if winning:
            return random.choice(winning)
 
        # Rule 2: block opponent's immediate win.
        blocking = find_winning_moves(board, opponent)
        if blocking:
            return random.choice(blocking)
 
        # Rule 3: prefer central columns.
        center = COLS // 2
        min_dist = min(abs(col - center) for col in moves)
        central_moves = [col for col in moves if abs(col - center) == min_dist]
 
        # Rule 4: among those, extend your own longest line.
        scored = []
        for col in central_moves:
            row = get_drop_row(board, col)
            test_board = simulate_move(board, col, player)
            line_len = self._longest_line_through_cell(test_board, row, col, player)
            scored.append((col, line_len))
 
        best_len = max(length for _, length in scored)
        best_moves = [col for col, length in scored if length == best_len]
 
        # Mandatory tie-breaking rule.
        return random.choice(best_moves)
 
    @staticmethod
    def _longest_line_through_cell(board, row, col, player):
        """
        Returns the length of the longest run of player's discs passing through (row, col), checking both directions along each of the 4 axes
        Assumes board[row][col] already equals player
        """
        best = 1
        for dr, dc in directions:
            count = 1
 
            r, c = row + dr, col + dc
            while is_valid(r, c) and board[r][c] == player:
                count += 1
                r += dr
                c += dc
 
            r, c = row - dr, col - dc
            while is_valid(r, c) and board[r][c] == player:
                count += 1
                r -= dr
                c -= dc
 
            best = max(best, count)
        return best



# Agent 3: Minimax
# Minimax with alpha-beta pruning and a windowed heuristic evaluation.
class MinimaxAgent:
    WIN_SCORE = 10_000_000
 
    # Tunable heuristic weights.
    SCORE_FOUR = 100_000
    SCORE_THREE_OPEN = 100
    SCORE_TWO_OPEN = 10
    SCORE_OPP_THREE_OPEN = -120
    SCORE_OPP_TWO_OPEN = -10
    CENTER_WEIGHT = 6
 
    def __init__(self, depth=4):
        self.depth = depth

 
    def get_move(self, board, player):
        moves = legal_moves(board)
 
        # If only one legal move, skip the search entirely.
        if len(moves) == 1:
            return moves[0]
 
        best_score = -math.inf
        best_moves = []
        alpha, beta = -math.inf, math.inf
 
        for col in moves:
            child = simulate_move(board, col, player)
            score = self._minimax_value(child, self.depth - 1, alpha, beta, False, player)
 
            if score > best_score:
                best_score = score
                best_moves = [col]
            elif score == best_score:
                best_moves.append(col)
 
            alpha = max(alpha, best_score)
 
        # Mandatory tie-breaking rule.
        return random.choice(best_moves)
 
    def _minimax_value(self, board, depth, alpha, beta, maximizing, player):
        """
        Returns the minimax value of board from player's perspective.
        maximizing indicates whether the side to move at this node is
        player (True) or the opponent (False)
        """
        opponent = get_opponent(player)
        winner = is_winner(board)
 
        if winner == player:
            return self.WIN_SCORE + depth  # prefer faster wins
        if winner == opponent:
            return -self.WIN_SCORE - depth  # prefer slower losses
        if is_draw(board):
            return 0
        if depth == 0:
            return self._score_position(board, player)
 
        moves = legal_moves(board)
 
        if maximizing:
            value = -math.inf
            for col in moves:
                child = simulate_move(board, col, player)
                value = max(value, self._minimax_value(child, depth - 1, alpha, beta, False, player))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # beta cut-off
            return value
        else:
            value = math.inf
            for col in moves:
                child = simulate_move(board, col, opponent)
                value = min(value, self._minimax_value(child, depth - 1, alpha, beta, True, player))
                beta = min(beta, value)
                if alpha >= beta:
                    break  # alpha cut-off
            return value
 
    def _score_position(self, board, player):
        """
        Full heuristic evaluation of board from player's perspective
        Goes over every (4-length) row, column, and diagonal 
        """
        score = 0
 
        # Centre-column control.
        center_col = [board[r][COLS // 2] for r in range(ROWS)]
        score += center_col.count(player) * self.CENTER_WEIGHT
 
        # Horizontal windows.
        for r in range(ROWS):
            row_array = board[r]
            for c in range(COLS - 3):
                window = row_array[c:c + 4]
                score += self._evaluate_window(window, player)
 
        # Vertical windows.
        for c in range(COLS):
            col_array = [board[r][c] for r in range(ROWS)]
            for r in range(ROWS - 3):
                window = col_array[r:r + 4]
                score += self._evaluate_window(window, player)
 
        # Diagonal down-right windows.
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                window = [board[r + i][c + i] for i in range(4)]
                score += self._evaluate_window(window, player)
 
        # Diagonal down-left (up-right) windows.
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                window = [board[r - i][c + i] for i in range(4)]
                score += self._evaluate_window(window, player)
 
        return score
 
    def _evaluate_window(self, window, player):
        """Scores a single length-4 window from `player`'s perspective."""
        opponent = get_opponent(player)
        score = 0
 
        player_count = window.count(player)
        opp_count = window.count(opponent)
        empty_count = window.count(EMPTY)
 
        if player_count == 4:
            score += self.SCORE_FOUR
        elif player_count == 3 and empty_count == 1:
            score += self.SCORE_THREE_OPEN
        elif player_count == 2 and empty_count == 2:
            score += self.SCORE_TWO_OPEN
 
        if opp_count == 3 and empty_count == 1:
            score += self.SCORE_OPP_THREE_OPEN
        elif opp_count == 2 and empty_count == 2:
            score += self.SCORE_OPP_TWO_OPEN
 
        return score
