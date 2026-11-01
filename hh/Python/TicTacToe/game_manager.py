from abc import ABC, abstractmethod, abstractclassmethod
from dataclasses import dataclass


@dataclass
class TicTacToeCell:
    """Dataclass for a single cell on the board
    
    Attributes:
        x (int): x coordinate on the board
        y (int): y coordinate on the board
        symbol (str): the value in the cell - 'X', 'O', or None
    """
    x: int
    y: int
    symbol: str
    
    """
        Change equals and hash to consider only symbols.
        This way, a set of cells 'shows' the symbols which appear in it.
    """
    
    def __eq__(self, other):
        if isinstance(other, TicTacToeCell):
            return self.symbol == other.symbol
        return False
    
    def __hash__(self):
        return self.symbol.__hash__()
    
    @property
    def coords(self):
        """The coordinates as a tuple (x, y)"""
        return self.x, self.y
    
    @property
    def is_empty(self):
        """True if the cell wasn't taken by either player (symbol is None)"""
        return self.symbol is None


class TicTacToeBoard:
    """
    Attributes:
        board (matrix of str): the cells of the board currently
    """
    
    """ The size of a tic tac toe board (assumes square)"""
    BOARD_SIZE = 3
    
    def clean_board(self):
        """Empties the board completely"""
        self.board = [[None] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
    
    def __init__(self):
        self.clean_board()
    
    def get(self, coords):
        """gets the cell from given coordinates

        Args:
            coords (tuple of int): x, y coordinates of the cell to fetch

        Returns:
            TicTacToeCell: A cell object for the given cell
        """
        x, y = coords
        return TicTacToeCell(x, y, self.board[y][x])
    
    def set(self, coords, sym):
        """Sets the symbol of a cell

        Args:
            coords (tuple of int): x, y coordinates of the cell to fetch
            sym (str): symbol to put at said cell

        Returns:
            bool: True if the assignment succeeded, False otherwise
        """
        try:
            x, y = coords
            self.board[y][x] = sym
            return True
        except Exception:
            return False
    
    @property
    def is_full(self):
        """True if all cells on the board aren't empty"""
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self.board[i][j] is None:
                    return False
        return True
    
    @property
    def win_axes(self):
        """Generator of all axes on which a player may win.
        
        Yields:
            list of TicTacToeCell: an axis which if all symbols on said axis
                were identical, a player would win.
        """
        for x in range(self.BOARD_SIZE):
            # rows
            yield [self.get((x, y)) for y in range(self.BOARD_SIZE)]
            # cols
            yield [self.get((y, x)) for y in range(self.BOARD_SIZE)]
        
        # primary diagonal
        yield [self.get((x, x)) for x in range(self.BOARD_SIZE)]

        # secondary diagonal
        yield [self.get((x, self.BOARD_SIZE - 1 - x)) for x in range(self.BOARD_SIZE)]   
    
    @property
    def winner(self):
        """The symbol of the winning player, None if no player won yet"""
        for axis in self.win_axes:
            if len(set(axis)) != 1:
                continue
            symbol = axis[0].symbol
            if symbol != None:
                return symbol

    def __repr__(self):
        res = ""
        for i, row in enumerate(self.board):
            if i > 0:
                res += ("---+" * (self.BOARD_SIZE - 1)) + "---\n"
            row_symbols = [' ' if sym is None else sym for sym in row]
            res += '|'.join([f' {sym} ' for sym in row_symbols]) + "\n"
        
        return res

class TicTacToeAgent(ABC):
    """Abstract base class for a Tic Tac Toe 'Player'.
    
    Represents an object which can generate moves.
    
    Attributes:
        symbol (str): the symbol of the agent on the board (their moves)
        bad_moves (int): the number of invalid moves made by the agent
    """
    MAX_BAD_MOVES = 3
    
    def __init__(self, symbol):
        self.symbol = symbol
        self.bad_moves = 0
                
    @abstractmethod
    def find_move(self, board):
        """Generates a move to play given a board state

        Args:
            board (TicTacToeBoard): the current game position
            
        Returns:
            tuple of int: the coordinates in which the next move should be played
        """
        pass          


class TicTacToeGame(ABC):
    """Abstract base class for a generic TicTacToe game between unknown agents.
    
    Attributes:
        players (list of TicTacToeAgent): the list of length 2 of two agent instances
            which play the current game.
        board (TicTacToeBoard): the current board position of the game 
    """
    symbols = ['X', 'O']
    
    @property
    @abstractclassmethod
    def player1_agent(cls):
        """Gets the class for the starting agent"""
        pass
    
    @property
    @abstractclassmethod
    def player2_agent(cls):
        """Gets the class for the second agent"""
        pass
    
    def __init__(self):
        player_agents = [self.player1_agent, self.player2_agent]
        self.players = [agent(sym) for agent, sym in zip(player_agents, self.symbols)]
        self.board = TicTacToeBoard()
    
    def start(self):
        """
            Manages play between the two agents.
            
            Returns:
                str (optional): the symbol of the winning player or None if a draw was reached
        """
        self.board.clean_board()
        self.taken_squares = set()
        current_player, next_player = self.players
        while self.board.winner is None and not self.board.is_full:
            # get the move from the player
            new_move = current_player.find_move(self.board)
            if new_move in self.taken_squares or \
                not self.board.set(new_move, current_player.symbol):
                # handle bad moves
                current_player.bad_moves += 1
                print(f"Bad Move for {current_player.symbol}! ({current_player.bad_moves}/{TicTacToeAgent.MAX_BAD_MOVES})")
                if current_player.bad_moves >= TicTacToeAgent.MAX_BAD_MOVES:
                    # if out of bad moves, other player wins
                    return next_player.symbol
                continue
            # mark square as taken
            self.taken_squares.add(new_move)
            # swap players
            current_player, next_player = next_player, current_player

        # return the winner        
        return self.board.winner
    
    def play(self):
        """
            Runs a game between the two agents and prints the result.
        """
        winner = self.start()
        print(self.board)
        if winner is None:
            print("Draw!")
        else:
            print(f"{winner} won!")

    @staticmethod
    def make(agent1, agent2):
        """A factory method for creating games between two agents

        Args:
            agent1 (class, extends TicTacToeAgent): The agent class for the starting player
            agent2 (class, extends TicTacToeAgent): The agent class for the second player

        Returns:
            TicTacToeGame: a game instance between a player of type agent1 and a player
                of type agent2.
        """
        class GameChild(TicTacToeGame):
            player1_agent = agent1
            player2_agent = agent2
            
        return GameChild()
