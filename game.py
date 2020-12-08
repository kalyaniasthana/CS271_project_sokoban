from board import Board
from copy import deepcopy
from heuristic import Heuristic
from priority_queue import PriorityQueue
from time import time

class Game:
	def __init__(self, board):
		self.board = board
		assert isinstance(self.board, Board)
		self.board.parse()
		self.board.make_board_grid()
		self.board.display_board()

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
			currentMove = path.pop(0)

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
						return 'SOLUTION FOUND!', ','.join(currentMove[1:] + [move]).replace(',',''), str((end - start)) + ' seconds'
						# return None
					if self.is_deadlock(childNode):
						print('DEADLOCK CONDITION')
						deadlockConditions += 1
						continue
					frontier1.append(childNode)
					frontier2.append((childNode.get_player_loc(), childNode.get_box_coordinates()))
					path.append(currentMove + [move])
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
		heuristicVal = H.calculate(rootNode.get_stor_coordinates(), rootNode.get_box_coordinates())

		frontier1 = PriorityQueue()
		frontier2 = PriorityQueue()
		path = PriorityQueue()

		frontier1.push(rootNode, heuristicVal)
		frontier2.push((rootNode.get_player_loc(), rootNode.get_box_coordinates()), heuristicVal)
		path.push([''], heuristicVal)
		visited = []

		deadlockConditions = 0

		while True:
			print('Generated Nodes: {}, Repeated Nodes: {}, Frontier Length: {}, Deadlock Conditions: {}'.format(
				generatedNodes, repeatedNodes, len(frontier1.Heap), deadlockConditions))
			if not frontier1.Heap:
				end = time()
				return 'SOLUTION NOT FOUND', (end - start)

			currentNode = frontier1.pop()
			(currentPlayer, currentBoxCoordinates) = frontier2.pop()
			currentMove = path.pop()

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
						return 'SOLUTION FOUND!', ','.join(currentMove[1:] + [move]).replace(',',''), str((end - start)) + ' seconds'
						# return None
					if self.is_deadlock(childNode):
						print('DEADLOCK CONDITION')
						deadlockConditions += 1
						continue

					heuristicVal = H.calculate(childNode.get_stor_coordinates(), childNode.get_box_coordinates())
					frontier1.push(childNode, heuristicVal)
					frontier2.push((childNode.get_player_loc(), childNode.get_box_coordinates()), heuristicVal)
					path.push(currentMove + [move], heuristicVal)
				else:
					repeatedNodes += 1

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
		if self.corner_deadlock(boardObject) or self.pre_corner_deadlock(boardObject) or self.square_block_deadlock(boardObject):
			return True
		return False