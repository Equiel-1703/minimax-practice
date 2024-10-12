from anytree import Node, RenderTree

def create_possibilities_tree(root: Node, gen_func, player_1, deep_max=5):
	new_states = gen_func(root.name, player_1)

	for s in new_states:
		Node(s, parent=root)
	
	if deep_max > 1:
		for c in root.children:
			create_possibilities_tree(c, gen_func, not player_1, deep_max=(deep_max-1))

def minimax(root: Node, score_func, is_max):
	if len(root.children) == 0:
		score = score_func(root.name)
		return (score, root.name.coord)
	
	if is_max:
		max_val_coord = root.children[0].name.coord
		max_val = minimax(root.children[0], score_func, not is_max)[0]

		for c in root.children[1:]:
			temp = minimax(c, score_func, not is_max)[0]
			if temp > max_val:
				max_val = temp
				max_val_coord = c.name.coord
		
		return (max_val, max_val_coord)
	else:
		min_val_coord = root.children[0].name.coord
		min_val = minimax(root.children[0], score_func, not is_max)[0]
		
		for c in root.children[1:]:
			temp = minimax(c, score_func, not is_max)[0]
			if temp < min_val:
				min_val = temp
				min_val_coord = c.name.coord
		
		return (min_val, min_val_coord)