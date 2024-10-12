from anytree import Node, RenderTree
import sys

def create_possibilities_tree(root: Node, gen_func, player_1: bool, deep_max=5):
	new_states = gen_func(root.name, player_1)

	for s in new_states:
		Node(s, parent=root)
	
	if deep_max > 1:
		for c in root.children:
			create_possibilities_tree(c, gen_func, not player_1, deep_max=(deep_max-1))

def minimax(root: Node, score_func, check_game_over_func, is_max=True):
	if len(root.children) == 0 or check_game_over_func(root.name):
		score = score_func(root.name)
		
		root.name.mm = score

		return (score, root.name.coord)
	
	if is_max:
		max_val_coord = (0,0)
		max_val = -(sys.maxsize - 1)

		for c in root.children:
			temp = int(minimax(c, score_func, check_game_over_func, is_max=False)[0])
			
			c.name.mm = temp

			if temp > max_val:
				max_val = temp
				max_val_coord = c.name.coord
		
		root.name.mm = max_val

		return (max_val, max_val_coord)
	else:
		min_val_coord = (0,0)
		min_val = sys.maxsize
		
		for c in root.children:
			temp = int(minimax(c, score_func, check_game_over_func, is_max=True)[0])

			c.name.mm = temp

			if temp < min_val:
				min_val = temp
				min_val_coord = c.name.coord
		
		root.name.mm = min_val

		return (min_val, min_val_coord)