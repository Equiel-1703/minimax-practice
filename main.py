from ttoe.TTToe import TTToe

import re
import os

# Check if the user is using Windows or not
if os.name == "nt":
	# If the OS is Windows, we must enable colors in the terminal
	os.system("color")

x_turn = True

game = TTToe()

while(True):
	if game.check_winner() == -1:
		print("Player 2 Wins")
		break
	elif game.check_winner() == 1:
		print(game)
		print("\nPlayer 1 Wins")
		break
	elif game.game_ended():
		print(game)
		print("Deu véia :D KKKKKKK")
		break
	
	if not x_turn:
		print(game)

		while(True):
			str_coords = input("Coord: ")
			int_coords = list(map(int, re.findall(r'\d+', str_coords)))

			if len(int_coords) < 2:
				if re.search(r'[xX]', str_coords):
					exit()
				continue
			else:
				try:
					game.play_o(int_coords[0] - 1, int_coords[1] - 1)
				except Exception as e:
					print(e)
					continue
				else:
					print("\n--- Sua jogada: \n")
					print(game)
					break
		print()
	else:
		# Get ai position
		ai_coord = game.get_minimax_coord(debug=True, deep=3)

		# Set position
		game.play_x(ai_coord[0], ai_coord[1])

		print("--- IA vai jogar ---")
		input()
	
	x_turn = not x_turn