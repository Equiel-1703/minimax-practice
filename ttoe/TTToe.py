import numpy as np
import copy
import anytree
import ttoe.minimax as minimax

EMPTY_SLOT = ' '
X_SLOT = 'X' # Player 1
O_SLOT = 'O'

class PositionOccupied(Exception):
	"""Exceção para posição ocupada no tabuleiro."""
	def __init__(self, pos) -> None:
		self.pos = pos
		self.message = f"A posição ({pos[0]}, {pos[1]}) está ocupada!"
		super().__init__(self.message)

class InvalidPosition(Exception):
	"""Exceção para posição fora do tabuleiro."""
	def __init__(self, pos) -> None:
		self.pos = pos
		self.message = f"A posição ({pos[0]}, {pos[1]}) é inválida!"
		super().__init__(self.message)

class Move:
	def __init__(self, coord, board: np.ndarray) -> None:
		self.coord = coord
		self.board = board
	
	def check_winner(move):
		matrix = move.board

		# Check rows
		for row in matrix:
			if all(cell == X_SLOT for cell in row):
				return 1
			if all(cell == O_SLOT for cell in row):
				return -1

		# Check columns
		for col in range(3):
			if all(matrix[row][col] == X_SLOT for row in range(3)):
				return 1
			if all(matrix[row][col] == O_SLOT for row in range(3)):
				return -1

		# Check diagonals
		if all(matrix[i][i] == X_SLOT for i in range(3)):
			return 1
		if all(matrix[i][i] == O_SLOT for i in range(3)):
			return -1
		
		if all(matrix[i][2 - i] == X_SLOT for i in range(3)):
			return 1
		if all(matrix[i][2 - i] == O_SLOT for i in range(3)):
			return -1

		return 0

class TTToe:
	def __init__(self, board=None) -> None:
		if board is None:
			self.__board = np.full((3, 3), EMPTY_SLOT)
		else:
			self.__board = board
		
		self.empty_slots = 0

		for l in self.__board:
			for c in l:
				if c == EMPTY_SLOT:
					self.empty_slots += 1
	
	def __str__(self) -> str:
		return TTToe.board_to_str(self.__board)

	def __play(self, l, c, slot):
		if l < 0 or l > 2 or c < 0 or c > 2:
			raise InvalidPosition((l + 1, c + 1))

		if self.__board[l, c] == EMPTY_SLOT:
			self.__board[l, c] = slot
			self.empty_slots -= 1
		else:
			raise PositionOccupied((l + 1, c + 1))

	def play_x(self, l, c):
		self.__play(l, c, X_SLOT)
	
	def play_o(self, l, c):
		self.__play(l, c, O_SLOT)
	
	def get_board(self):
		return self.__board
	
	def get_possible_moves(move, player_1):
		board = move.board
		moves = []
		
		for l in range(3):
			for c in range(3):
				if board[l, c] == EMPTY_SLOT:
					board[l, c] = X_SLOT if player_1 else O_SLOT

					moves.append(Move((l, c), copy.deepcopy(board)))
					
					board[l, c] = EMPTY_SLOT
		
		return moves

	def check_winner(self):
		return Move.check_winner(Move((0,0), self.__board))
	
	def game_ended(self) -> bool:
		return self.empty_slots <= 0

	def get_minimax_coord(self) -> tuple:
		tree = anytree.Node(Move((0,0), self.__board))
		minimax.create_possibilities_tree(tree, TTToe.get_possible_moves, True, deep_max=6)
		return minimax.minimax(tree, Move.check_winner, True)[1]
	
	def board_to_str(board: np.ndarray) -> str:
		out_strs = []
		out_strs.append("  1 2 3\n")
		for l in range(3):
			# Print line number
			out_strs.append(str(l + 1) + " ")
			# Print line content
			for c in range(3):
				out_strs.append(board[l, c])
				if c < 2:
					out_strs.append("│")
			# Print line separtions
			if l < 2:
				out_strs.append("\n  ─┼─┼─\n")
		
		return ''.join(out_strs)
	
		minimax