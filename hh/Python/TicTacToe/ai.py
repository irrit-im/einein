from game_manager import TicTacToeAgent

"""
    The list of cells on the board, prioritized from worst to best according to the bot
"""
PRIORITIZED_CELLS = [
    (1, 1), # center is best
    (0, 0), (0, 2), (2, 0), (2, 2), # then corners
    (0, 1), (1, 0), (1, 2), (2, 1)  # then edges
]

class TicTacToeBot(TicTacToeAgent):
    """
        An unbeatable TicTacToeAgent. Cannot lose :)
    """
    def __init__(self, symbol):
        super().__init__(symbol)
    
    def _is_blocking(self, symbol, check_enemy=False):
        """Helper method, checks if a symbol blocks a win for a player
        (if check_enemy=True, checks for blocking enemy win)"""
        if check_enemy:
            return symbol == self.symbol
        else:
            return symbol not in [None, self.symbol]
        
    def _find_win(self, board, check_enemy=False):
        """Helper method. Attempts to find a winning move for a player on the board.
        If check_enemy=True, looks for a winning move for the enemy. """
        for axis in board.win_axes:
            symbols = [cell.symbol for cell in axis]
            if any([self._is_blocking(sym, check_enemy) for sym in symbols]):
                continue
            if symbols.count(None) != 1:
                continue
            return axis[symbols.index(None)].coords
    
    def _try_win(self, board):
        """A tactic, attempts to find an immediate winning move (win in the next move).
        
        Args:
            board (TicTacToeBoard): the current game position.
        
        Returns:
            tuple of int (optional): the coordinates of a winning move, or None if no winning move exists
        """
        return self._find_win(board)
    
    def _stop_enemy_win(self, board):
        """A tactic, attempts to block an enemy's win (win in the next move).
        
        Args:
            board (TicTacToeBoard): the current game position.
        
        Returns:
            tuple of int (optional): the coordinates of a winning move for the enemy,
                or None if no winning move exists for the enemy.
        """
        return self._find_win(board, check_enemy=True)
    
    def _find_forks(self, board, check_enemy=False):
        """A helper method which returns a list of coordinates which give the player a fork.
        A fork is two independent winning moves on the next half-turn.
        (if check_enemy=True, checks for blocking enemy win)"""
        threat_mat = [[False] * board.BOARD_SIZE for _ in range(board.BOARD_SIZE)]
        fork_threats = []
        for axis in board.win_axes:
            # if putting in axis makes a threat
            if all([cell.is_empty for cell in axis]) or \
               any([self._is_blocking(cell.symbol, check_enemy) for cell in axis]):
                continue
            # mark empty cells as threat
            for cell in axis:
                if not cell.is_empty:
                    continue
                if threat_mat[cell.x][cell.y]:
                    # double threat is fork
                    fork_threats.append(cell.coords)
                else:
                    threat_mat[cell.x][cell.y] = True
        return fork_threats
    
    def _try_fork(self, board):
        """A tactic, attempts to create a fork.

        Args:
            board (TicTacToeBoard): the current game position.

        Returns:
            tuple of int (optional): the coordinates of a forking move, or None if no
                forking moves exist.
        """
        fork_threats = self._find_forks(board)
        if len(fork_threats) == 0:
            return None
        return fork_threats[0]
    
    def _stop_enemy_fork(self, board):
        """A tactic, attempts to block enemy forks.

        Args:
            board (TicTacToeBoard): the current game position.

        Returns:
            tuple of int (optional): the coordinates of a move which should prevent enemy forks
                (on the next turn), None if no preventing move was found.
        """
        enemy_forks = self._find_forks(board, check_enemy=True)
        
        if len(enemy_forks) == 0:
            return None
        
        for axis in board.win_axes:
            # if putting in axis makes a threat
            if all([cell.is_empty for cell in axis]) or \
               any([self._is_blocking(cell.symbol) for cell in axis]):
                continue
            # looks for threat which can't be blocked with a fork
            empty_cells = [cell for cell in axis if cell.is_empty]
            for cell in empty_cells:
                other_empty = [other for other in empty_cells if other.coords != cell.coords]
                if all([other.coords not in enemy_forks for other in other_empty]):
                    return cell.coords
        
    # Implements the abstract method for TicTacToeAgent
    def find_move(self, board):
        # try to act according to tactics
        prioritized_tactics = [
            self._try_win,
            self._stop_enemy_win,
            self._try_fork,
            self._stop_enemy_fork
        ]
        for tactic in prioritized_tactics:
            my_move = tactic(board)
            if my_move is not None:
                return my_move
        
        # tactic not found, pick prioritized cell
        for coords in PRIORITIZED_CELLS:
            if board.get(coords).is_empty:
                return coords
