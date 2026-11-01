from game_manager import TicTacToeAgent, TicTacToeGame
from ai import TicTacToeBot

class TicTacToeHuman(TicTacToeAgent):
    """A TicTacToeAgent which represents a human player."""
    def find_move(self, board):
        print(board)
        input_line = input(f"Make a move as {self.symbol} (x and y coords, formatted as \"x, y\", numbers from 0 to {board.BOARD_SIZE - 1}): ")
        str_coords = input_line.split(',')
        if len(str_coords) != 2:
            return None
        try:
            return tuple(int(coord) for coord in str_coords)
        except ValueError:
            return None

if __name__ == '__main__':
    TicTacToeGame.make(TicTacToeHuman, TicTacToeBot).play()