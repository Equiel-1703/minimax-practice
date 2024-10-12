import numpy as np
import copy
import anytree
import ttoe.minimax as minimax
import sys
from ttoe.terminal_colors import TerminalColors as tc

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

class MMElement:
	def __init__(self, coord, board: np.ndarray, mm:int = -(sys.maxsize - 1)) -> None:
		self.coord = coord
		self.board = board
		self.mm = mm
	
	def check_game_over(el):
		board = el.board
		free_slots = 0

		for l in board:
			for c in l:
				if c == EMPTY_SLOT:
					free_slots += 1
		
		winner = MMElement.check_winner(el)

		return (free_slots == 0) or (winner != 0)

	def check_winner(el) -> int:
		matrix = el.board

		# Check rows
		for row in matrix:
			if all(cell == X_SLOT for cell in row):
				return 1
			elif all(cell == O_SLOT for cell in row):
				return -1

		# Check columns
		for col in range(3):
			if all(matrix[row][col] == X_SLOT for row in range(3)):
				return 1
			elif all(matrix[row][col] == O_SLOT for row in range(3)):
				return -1

		# Check diagonals
		if all(matrix[i][i] == X_SLOT for i in range(3)):
			return 1
		elif all(matrix[i][i] == O_SLOT for i in range(3)):
			return -1
		
		if all(matrix[i][2 - i] == X_SLOT for i in range(3)):
			return 1
		elif all(matrix[i][2 - i] == O_SLOT for i in range(3)):
			return -1

		# Ninguém ganhou
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

					moves.append(MMElement((l, c), copy.deepcopy(board)))
					
					board[l, c] = EMPTY_SLOT
		
		return moves

	def check_winner(self) -> int:
		return MMElement.check_winner(MMElement((0,0), self.__board))
	
	def game_ended(self) -> bool:
		return self.empty_slots <= 0

	def get_minimax_coord(self, deep=2, debug=False, player_1=True) -> tuple:
		tree = anytree.Node(MMElement((0,0), self.__board))
		minimax.create_possibilities_tree(tree, TTToe.get_possible_moves, player_1, deep_max=deep)

		coord = minimax.minimax(tree, MMElement.check_winner, MMElement.check_game_over, is_max=player_1)[1]

		if debug:
			for pre, _, content in anytree.RenderTree(tree):
				print(f"{pre}{TTToe.board_to_line_str(content.name.board)} Coord: {content.name.coord} Score: {int(content.name.mm)}")

		return coord
	
	def board_to_line_str(board: np.ndarray):
		out_str = []
		lines_colors = [tc.HEADER, tc.OKBLUE, tc.WARNING]

		for i in range(3):
			out_str.append(lines_colors[i])
			
			for j in range(3):
				out_str.append(board[i, j])
				out_str.append('-')
			
			out_str.append(tc.ENDC)
		
		out_str.pop(-2)

		return (''.join(out_str)).strip()

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