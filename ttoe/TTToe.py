import numpy as np

EMPTY_SLOT = ' '
X_SLOT = 'X'
O_SLOT = 'O'

class TTToe:
	def __init__(self) -> None:
		self.__board = np.full((3, 3), EMPTY_SLOT)
	
	def print(self):
		print("  1 2 3")
		for l in range(3):
			# Print line number
			print(str(l + 1), end=" ")
			# Print line content
			for c in range(3):
				print(self.__board[l, c], end="")
				if c < 2:
					print("│", end="")
			# Print line separtions
			if l < 2:
				print("\n  ─┼─┼─")