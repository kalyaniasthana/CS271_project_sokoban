from board import Board
from copy import deepcopy
from heuristic import Heuristic
from math import ceil
from priority_queue import PriorityQueue
from time import time

FOUND = float('Inf')
NOT_FOUND = float('-Inf')

class Game:
	def __init__(self, board):
		self.board = board
		assert isinstance(self.board, Board)
		self.board.parse()
		self.board.make_board_grid()
		self.board.display_board()
		self.branchingFactor, self.treeDepth = 0, 0

	def play_moves(self, moves):
		if moves: # moves is a list of moves/actions. For example, moves = ['l', 'u', 'U', 'U', 'U']
			for move in moves:
				if self.board.update_board(move):
					self.board.make_board_grid()
					self.board.display_board()
					# print(sokoban_board)
					print('-'*20)
					print(self.board.possible_moves(), "<--POSSIBLE MOVES")
				else:
					print("COULD NOT UPDATE BOARD!")
				if self.board.is_goal_state():
					print("REACHED GOAL STATE!")
					break

	def play_BFS(self):
		start = time()

		rootNode = deepcopy(self.board)
		generatedNodes, repeatedNodes = 1, 0

		if not rootNode.get_stor_coordinates():
			end = time()
			return 'THERE ARE NO STORAGE LOCATIONS!', (end - start)
		if not rootNode.get_box_coordinates():
			end = time()
			return 'THERE ARE NO BOX LOCATIONS!', (end - start)
		if not rootNode.get_player_loc():
			end = time()
			return 'SOKOBAN PLAYER MISSING!', (end - start)
		if rootNode.is_goal_state():
			end = time()
			return 'BOARD IS ALREADY IN GOAL STATE!', (end - start)

		frontier1 = [rootNode]
		# we need another frontier since with player and box locations since deepcopy() created a new object
		# with a new pointer each time
		frontier2 = [(rootNode.get_player_loc(), rootNode.get_box_coordinates())]
		path = [['']]
		visited = []

		deadlockConditions = 0

		while True:
			print('Generated Nodes: {}, Repeated Nodes: {}, Frontier Length: {}, Deadlock Conditions: {}'.format(
				generatedNodes, repeatedNodes, len(frontier1), deadlockConditions))
			if not frontier1:
				end = time()
				return 'SOLUTION NOT FOUND', (end - start)

			currentNode = frontier1.pop(0)
			(currentPlayer, currentBoxCoordinates) = frontier2.pop(0)
			currentActionSequence = path.pop(0)

			possibleMoves = currentNode.possible_moves()
			visited.append((currentPlayer, currentBoxCoordinates))

			for move in possibleMoves:
				childNode = deepcopy(currentNode)
				generatedNodes += 1
				childNode.update_board(move)
				if (childNode.get_player_loc(), childNode.get_box_coordinates()) not in visited:
					if childNode.is_goal_state():
						childNode.make_board_grid()
						childNode.display_board()
						end = time()
						return 'SOLUTION FOUND!', ','.join(currentActionSequence[1:] + [move]).replace(',',''), str((end - start)) + ' seconds'
						# return None
					if self.is_deadlock(childNode):
						print('DEADLOCK CONDITION')
						deadlockConditions += 1
						continue
					frontier1.append(childNode)
					frontier2.append((childNode.get_player_loc(), childNode.get_box_coordinates()))
					path.append(currentActionSequence + [move])
				else:
					repeatedNodes += 1

	def play_AStar(self):
		start = time()

		rootNode = deepcopy(self.board)
		generatedNodes, repeatedNodes = 1, 0

		if not rootNode.get_stor_coordinates():
			end = time()
			return 'THERE ARE NO STORAGE LOCATIONS!', (end - start)
		if not rootNode.get_box_coordinates():
			end = time()
			return 'THERE ARE NO BOX LOCATIONS!', (end - start)
		if not rootNode.get_player_loc():
			end = time()
			return 'SOKOBAN PLAYER MISSING!', (end - start)
		if rootNode.is_goal_state():
			end = time()
			return 'BOARD IS ALREADY IN GOAL STATE!', (end - start)

		H = Heuristic()
		# H.set_heuristic("manhattan2")
		heuristicVal = H.calculate(rootNode.get_stor_coordinates(), rootNode.get_box_coordinates())

		frontier1 = PriorityQueue()
		frontier2 = PriorityQueue()
		path = PriorityQueue()

		frontier1.push(rootNode, heuristicVal)
		frontier2.push((rootNode.get_player_loc(), rootNode.get_box_coordinates()), heuristicVal)
		path.push([''], heuristicVal)
		visited = []

		deadlockConditions = 0

		# Hamza: This i represents the number of states visited, I think generated Nodes does not apply because
		# we don't explore possible moves for all of the generated nodes so the branching factor cannot use this value
		# i, b = 0, 0 # don't really need i since we can just do len(visited) for this
		b = 0
		self.branchingFactor = 0
		self.treeDepth = 0

		while True:
			print('Generated Nodes: {}, Repeated Nodes: {}, Frontier Length: {}, Deadlock Conditions: {}'.format(
				generatedNodes, repeatedNodes, len(frontier1.Heap), deadlockConditions))
			if not frontier1.Heap:
				end = time()
				return 'SOLUTION NOT FOUND', (end - start)

			currentNode = frontier1.pop()
			(currentPlayer, currentBoxCoordinates) = frontier2.pop()
			currentActionSequence = path.pop()

			possibleMoves = currentNode.possible_moves()
			visited.append((currentPlayer, currentBoxCoordinates))

			# Tree depth and branch factor variables
			b += len(possibleMoves) # branching factor of the current node
			# i = len(visited) # number of visited nodes
			self.treeDepth += 1

			for move in possibleMoves:
				childNode = deepcopy(currentNode)
				generatedNodes += 1
				childNode.update_board(move)
				if (childNode.get_player_loc(), childNode.get_box_coordinates()) not in visited:
					if childNode.is_goal_state():
						childNode.make_board_grid()
						childNode.display_board()
						end = time()
						self.branchingFactor = ceil(b/len(visited))# average branching factor
						return  str(len(currentActionSequence[1:] + [move])) + ' ' + ''.join(map(lambda x:x.upper(), currentActionSequence[1:] + [move])).replace(',','') #, str((end - start)) + ' seconds'
						# return None
					if self.is_deadlock(childNode):
						print('DEADLOCK CONDITION')
						deadlockConditions += 1
						continue

					heuristicVal = H.calculate(childNode.get_stor_coordinates(), childNode.get_box_coordinates())
					cost = self.compute_cost(currentActionSequence + [move])
					# childNode.make_board_grid()
					# childNode.display_board()
					frontier1.push(childNode, heuristicVal + cost)
					frontier2.push((childNode.get_player_loc(), childNode.get_box_coordinates()), heuristicVal + cost)
					path.push(currentActionSequence + [move], heuristicVal + cost)
				else:
					repeatedNodes += 1

	# def play_AStar_fix_f(self):
	# 	start = time()

	# 	rootNode = deepcopy(self.board)
	# 	generatedNodes, repeatedNodes = 1, 0

	# 	if not rootNode.get_stor_coordinates():
	# 		end = time()
	# 		return 'THERE ARE NO STORAGE LOCATIONS!', (end - start)
	# 	if not rootNode.get_box_coordinates():
	# 		end = time()
	# 		return 'THERE ARE NO BOX LOCATIONS!', (end - start)
	# 	if not rootNode.get_player_loc():
	# 		end = time()
	# 		return 'SOKOBAN PLAYER MISSING!', (end - start)
	# 	if rootNode.is_goal_state():
	# 		end = time()
	# 		return 'BOARD IS ALREADY IN GOAL STATE!', (end - start)

	# 	H = Heuristic()
	# 	# H.set_heuristic("manhattan2")
	# 	heuristicVal = H.calculate(rootNode.get_stor_coordinates(), rootNode.get_box_coordinates())
	# 	g = 0
	# 	frontier1 = PriorityQueue()
	# 	frontier2 = PriorityQueue()
	# 	path = PriorityQueue()

	# 	frontier1.push(rootNode, heuristicVal)
	# 	frontier2.push((rootNode.get_player_loc(), rootNode.get_box_coordinates()), g + heuristicVal)
	# 	path.push([''], g + heuristicVal)
	# 	visited = []

	# 	deadlockConditions = 0

	# 	# Hamza: This i represents the number of states visited, I think generated Nodes does not apply because
	# 	# we don't explore possible moves for all of the generated nodes so the branching factor cannot use this value
	# 	# i, b = 0, 0 # don't really need i since we can just do len(visited) for this
	# 	b = 0
	# 	self.branchingFactor = 0
	# 	self.treeDepth = 0

	# 	while True:
	# 		print('Generated Nodes: {}, Repeated Nodes: {}, Frontier Length: {}, Deadlock Conditions: {}'.format(
	# 			generatedNodes, repeatedNodes, len(frontier1.Heap), deadlockConditions))
	# 		if not frontier1.Heap:
	# 			end = time()
	# 			return 'SOLUTION NOT FOUND', (end - start)

	# 		currentNode = frontier1.pop()
	# 		(currentPlayer, currentBoxCoordinates) = frontier2.pop()
	# 		currentActionSequence = path.pop()

	# 		possibleMoves = currentNode.possible_moves()
	# 		visited.append((currentPlayer, currentBoxCoordinates))

	# 		# Tree depth and branch factor variables
	# 		b += len(possibleMoves) # branching factor of the current node
	# 		# i = len(visited) # number of visited nodes
	# 		self.treeDepth += 1

	# 		for move in possibleMoves:
	# 			childNode = deepcopy(currentNode)
	# 			generatedNodes += 1
	# 			childNode.update_board(move)
	# 			if (childNode.get_player_loc(), childNode.get_box_coordinates()) not in visited:
	# 				if childNode.is_goal_state():
	# 					childNode.make_board_grid()
	# 					childNode.display_board()
	# 					end = time()
	# 					self.branchingFactor = ceil(b/len(visited))# average branching factor
	# 					return 'SOLUTION FOUND!', ','.join(currentActionSequence[1:] + [move]).replace(',',''), str((end - start)) + ' seconds'
	# 					# return None
	# 				if self.is_deadlock(childNode):
	# 					print('DEADLOCK CONDITION')
	# 					deadlockConditions += 1
	# 					continue
	# 				heuristicVal = H.calculate(childNode.get_stor_coordinates(), childNode.get_box_coordinates())
	# 				childNode.make_board_grid()
	# 				childNode.display_board()
	# 				g = len(currentActionSequence)
	# 				g2 = self.compute_cost(currentActionSequence)
	# 				frontier1.push(childNode, heuristicVal + g2 + 1)
	# 				frontier2.push((childNode.get_player_loc(), childNode.get_box_coordinates()), heuristicVal + g2 + 1)
	# 				path.push(currentActionSequence + [move], heuristicVal + g2 + 1)
	# 			else:
	# 				repeatedNodes += 1

	def compute_cost(self, actions):
		cost = 0
		for action in actions:
			if action.islower():
				cost += 1
		return cost

	def corner_deadlock(self, boardObject):
		boardObject.make_board_grid()
		boardGrid = boardObject.get_board_grid()
		h = boardObject.get_sizeH()
		v = boardObject.get_sizeV()
		boxCoordinates = boardObject.get_box_coordinates()
		for coord in boxCoordinates:
			(i, j) = (coord[0], coord[1])
			if (boardGrid[i-1][j] == '#' and boardGrid[i][j-1] == '#'):
				return True
			elif (boardGrid[i+1][j] == '#' and boardGrid[i][j-1] == '#'):
				return True
			elif (boardGrid[i][j+1] == '#' and boardGrid[i-1][j] == '#'):
				return True
			elif (boardGrid[i][j+1] == '#' and boardGrid[i+1][j] == '#'):
				return True
		return False

	def pre_corner_deadlock(self, boardObject):
		"""It's one of these cases (same vertically):

			#      $                #     ##################...###
			 ##################...###     #          $           #
			 And there is no goal on the axis
		"""
		boardObject.make_board_grid()
		boardGrid = boardObject.get_board_grid()
		h = boardObject.get_sizeH()
		v = boardObject.get_sizeV()
		boxCoordinates = boardObject.get_box_coordinates()
		storCoordinates = boardObject.get_stor_coordinates()
		for coord in boxCoordinates:
			(i, j) = (coord[0], coord[1])
			if j == 0 or j == (h-1):
				for store in storCoordinates:
					if store[1] == 0 or store[1] == (v-1):
						if store[0] >= 0 or store[0] <= (h-1):
							return False
						return True

			elif i == 0 or i == (v-1):
				for store in storCoordinates:
					if store[0] == 0 or store[0] == (h-1):
						if store[1] >= 0 or store[1] <= (v-1):
							return False
						return True
		return False

	def pre_corner_deadlock2(self, boardObject):
		boardObject.make_board_grid()
		boardGrid = boardObject.get_board_grid()
		h = boardObject.get_sizeH()
		v = boardObject.get_sizeV()
		boxCoordinates = boardObject.get_box_coordinates()
		storCoordinates = boardObject.get_stor_coordinates()
		for coord in boxCoordinates:
			left_wall = False
			right_wall = False
			(m, n) = (coord[0], coord[1])
			for k in range(n):
				if not left_wall:
					if boardGrid[m][n-k-1] == '#':
						left_wall = True
						left_wall_coord = n-k-1
				if not right_wall:
					if n+k < h:
						if boardGrid[m][n+k] == '#':
							right_wall = True
							right_wall_coord = n+k
			if left_wall and right_wall:
				# This means we have this  # (free floor) $ (free floor)#
				upper_bound = True
				lower_bound = True
				for i in range(left_wall_coord+1, right_wall_coord):
					# upper bound
					if boardGrid[m-1][i] != '#':
						upper_bound = False
					if boardGrid[m+1][i] != '#':
						lower_bound = False
				if upper_bound:
					# This means we have this  #######(walls)###########
					#						  #(free floor)$(free floor)#
					for store in storCoordinates:
						if store[0] == m:
							if store[1] > left_wall_coord and store[1] < right_wall_coord:
								# There is a storLocation between the two places so there is no deadlock
								return False
					# print("WE HAVE AN UPPER DEADLOCK!")
					# boardObject.display_board()
					# print(" ")
					# print(" ")
					return True
				if lower_bound:
					# This means we have this  #(free floor)$(free floor)#
					#						    ########(walls)##########
					for store in storCoordinates:
						if store[0] == n:
							if store[1] > left_wall_coord and store[1] < right_wall_coord:
								# There is a storLocation between the two places so there is no deadlock
								return False
					return True
			# Now let's flip the board and check the same vertically
			upper_wall = False
			lower_wall = False
			for l in range(m):
				if not upper_wall:
					if boardGrid[m-l-1][n] == '#':
						upper_wall = True
						upper_wall_coord = m-l-1
				if not lower_wall:
					if m+l < v:
						if boardGrid[m+l][n] == '#':
							lower_wall = True
							lower_wall_coord = m+l
			if upper_wall and lower_wall:
				right_bound = True
				left_bound = True
				for i in range(upper_wall_coord+1, lower_wall_coord):
					if boardGrid[i][n+1] != '#':
						right_bound = False
					if boardGrid[i][n-1] != '#':
						left_bound = False
				if right_bound:
					for store in storCoordinates:
						if store[1] == n:
							if store[0] > upper_wall_coord and store[0] < lower_wall_coord:
								# There is a storLocation between the two places so there is no deadlock
								return False
					return True
				if left_bound:
					for store in storCoordinates:
						if store[0] == n:
							if store[1] > upper_wall_coord and store[1] < lower_wall_coord:
								# There is a storLocation between the two places so there is no deadlock
								return False
					return True
		return False

	def square_block_deadlock(self, boardObject):
		boardObject.make_board_grid()
		boardGrid = boardObject.get_board_grid()
		h = boardObject.get_sizeH()
		v = boardObject.get_sizeV()
		for i in range(v-1):
			for j in range(h-1):
				if boardGrid[i][j] == '$':
					if boardGrid[i+1][j] == '$' and boardGrid[i][j+1] == '$' and boardGrid[i+1][j+1] == '$':
						return True
					if boardGrid[i][j-1] == '$' and boardGrid[i+1][j] == '$' and boardGrid[i+1][j-1] == '$':
						return True
					if boardGrid[i-1][j] == '$' and boardGrid[i][j-1] == '$' and boardGrid[i-1][j-1] == '$':
						return True
					if boardGrid[i-1][j] == '$' and boardGrid[i-1][j+1] == '$' and boardGrid[i][j+1] == '$':
						return True
		return False

	def is_deadlock(self, boardObject):
		if self.corner_deadlock(boardObject) or self.pre_corner_deadlock(boardObject) or \
		self.square_block_deadlock(boardObject) or self.pre_corner_deadlock2(boardObject):
			return True
		return False


	###### EXPERIMENTAL ZONE ######

	def manhattan3_heuristic(self, boxCoordinates, storCoordinates, playerLoc):
		heuristicVal = 0
		if self.name == "manhattan" or self.name == None:
			for box in boxCoordinates:
				smallestBoxDist = float('Inf')
				smallestBoxCoordToPlayer = (0,0)
				for storage in storCoordinates:
					heuristicVal += (abs(storage[0] - box[0])+abs(storage[1] - box[1])) # WHAT THE HECK DO storage() AND box() RETURN?
				distance_box_to_player = (abs(playerLoc[0] - box[0])+abs(storage[1] - playerLoc[1]))
				if dist_box_to_storage < smallestBoxDist:
					smallestBoxDist =  dist_box_to_storage
					smallestBoxCoordToPlayer = box
			heuristicVal += smallestBoxDist

	def manhattan4_heuristic(self, boxCoordinates, storCoordinates):
		if self.name == "manhattan3":
			boxes = deepcopy(boxCoordinates)
			stores = deepcopy(storCoordinates)
			for box in boxes:
				smallestBoxDist = float('Inf')
				smallestStorCoord = (0, 0)
				for storage in stores:
					dist_box_to_storage = (abs(storage[0] - box[0])+abs(storage[1] - box[1]))
					if dist_box_to_storage < smallestBoxDist:
						smallestBoxDist =  dist_box_to_storage
						smallestStorCoord = storage
				boxCopy = boxCoordinates
				boxCopy.remove(box)
				for box_2 in boxCopy:
					dist_box_2_to_storage = (abs(smallestStorCoord[0] - box_2[0])+abs(smallestStorCoord[1] - box_2[1]))
					if dist_box_2_to_storage < smallestBoxDist:
						storCopy = storCoordinates
						storCopy.remove(smallestStorCoord)
						heuristicVal += dist_box_2_to_storage
						boxes.remove(box_2)
						boxCopy.remove(box_2)
						for store_2 in storeCopy:
							dist_box_to_storage = (abs(store_2[0] - box[0])+abs(store_2[1] - box[1]))
							if dist_box_to_storage < smallestBoxDist:
								smallestBoxDist =  dist_box_to_storage
								smallestStorCoord = storage
				stores.remove(smallestStorCoord)
				heuristicVal += smallestBoxDist

	#Push heuristic
	def update_directions(self, currentPos, smallestStorCoord):
		# if x_direction is True we move right, else left
		if currentPos[0] - smallestStorCoord[0] > 0:
			# Closest Stor Location is at left
			x_direction = False
		else:
			x_direction = True

		# if y_direction is True we move down, else up
		if currentPos[1] - smallestStorCoord[1] > 0:
			# Closest Stor Location is up
			y_direction = False
		else:
			y_direction = True

		return x_direction, y_direction

	def compute_pushHeuristic(self, boardObject):
		pushes = 0
		storCoordinates = boardObject.get_stor_coordinates()
		boxCoordinates = boardObject.get_box_coordinates()
		boardGrid = boardObject.get_board_grid()
		h = boardObject.get_sizeH()
		v = boardObject.get_sizeV()
		for box in boxCoordinates:
			print(box)
			smallestBoxDist = float('Inf')
			smallestStorCoord = (0,0)
			for storage in storCoordinates:
				dist_box_to_storage = (abs(storage[0] - box[0])+abs(storage[1] - box[1]))
				if dist_box_to_storage < smallestBoxDist:
					smallestBoxDist =  dist_box_to_storage
					smallestStorCoord = storage
			print(smallestStorCoord)
			currentPos = box
			x_direction, y_direction = self.update_directions(currentPos, smallestStorCoord)
			tries = 0
			while currentPos[0] != smallestStorCoord[0] and currentPos[1] != smallestStorCoord[1] or tries > 100:
				tries += 1
				x = currentPos[0]
				y = currentPos[1]
				if y_direction:
					# moving down!
					if y + 1 < v-1:
						if boardGrid[x+1][y] != '#' and boardGrid[x+1][y] != '$':
							currentPos = (x + 1, currentPos[1])
							pushes += 1
							x_direction, y_direction = self.update_directions(currentPos, smallestStorCoord)
					else:
						y_direction = False
				else:
					# moving up!
					if x - 1 > 0:
						if boardGrid[x-1][y] != '#' and boardGrid[x-1][y] != '$':
							currentPos = (x - 1, currentPos[1])
							pushes += 1
							x_direction, y_direction = self.update_directions(currentPos, smallestStorCoord)
					else:
						y_direction = True
				if x_direction:
					# moving right!
					if y + 1 < h-1:
						if boardGrid[x][y+1] != '#' and boardGrid[x+1][y+1] != '$':
							currentPos = (currentPos[0], y + 1)
							pushes += 1
							x_direction, y_direction = self.update_directions(currentPos, smallestStorCoord)
					else:
						x_direction = False
				else:
					# moving left!
					if y - 1 >= 0:
						if boardGrid[x][y] != '#' and boardGrid[x-1][y-1] != '$':
							currentPos = (currentPos[0], y - 1)
							pushes += 1
							x_direction, y_direction = self.update_directions(currentPos, smallestStorCoord)

					else:
						x_direction = True
		return pushes
