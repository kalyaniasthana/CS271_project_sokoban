from copy import deepcopy
import heapq # min-heap by default
import os # will mostly use this to NOT hard code paths
from time import time

class Board:

	def __init__(self, boardInputFile):
		# initialise board variables
		self.sizeH, self.sizeV, self.nWallSquares, self.wallCoordinates, self.nBoxes, \
		self.boxCoordinates, self.nstorLocations, self.storCoordinates, self.playerLoc = \
		None, None, None, None, None, None, None, None, None
		self.boardInputFile, self.boardGrid = boardInputFile, None
		self.actions = {"u": (-1,0), "U": (-1,0), "l": (0,-1), "L": (0,-1), "d": (1,0), "D": (1,0), "r": (0,1), "R": (0,1)}

	def __str__(self):
		"""display class variables"""
		return "sizeH: {self.sizeH}, sizeV: {self.sizeV}, nWallSquares: {self.nWallSquares}, wallCoordinates: {self.wallCoordinates}, nBoxes: {self.nBoxes}, boxCooridates: {self.boxCoordinates}, nstorLocations: {self.nstorLocations}, storCoordinates: {self.storCoordinates}, playerLoc: {self.playerLoc}'.format(self = self)"

	def get_sizeH(self):
		return self.sizeH

	def get_sizeV(self):
		return self.sizeV

	def get_nWall_squares(self):
		return self.nWallSquares

	def get_wall_coordatinates(self):
		return self.wallCoordinates

	def get_nBoxes(self):
		return self.nBoxes

	def get_box_coordinates(self):
		return self.boxCoordinates

	def get_nStor_locations(self):
		return self.nstorLocations

	def get_stor_coordinates(self):
		return self.storCoordinates

	def get_player_loc(self):
		return self.playerLoc

	def get_board_grid(self):
		return self.boardGrid

	def string_to_int_list(self, stringList):
		return list(map(int, stringList))

	def group_coordinates(self, n, coordList):
		"""newCoordList is a list of tuples. I think it's a good idea to use tuples for positions in the game board.
		The initial position of sokoban is also a tuple (x,y)"""
		newCoordList = []
		for i in range(0, n*2, 2):
			# -1 to match python array indices
			newCoordList.append((coordList[i] - 1, coordList[i+1] - 1))
		return newCoordList

	def parse(self): # parse input file - sokobanXY.txt
		"""input is expected to have 5 lines
		line 1 is the sizeH, sizeV
		line 2 is nWallSquares followed by a list wallCoordinates
		line 3 is a list of boxCordinates
		line 4 is a list of storCoordinates (storage location coordinates)
		line 5 is the initial position of SOKOBAN"""

		lineNumber = 1 # to iterate through the lines
		with open(self.boardInputFile) as f:
			for line in f:

				l_line = line.split(' ')

				if lineNumber == 1:
					self.sizeH, self.sizeV = int(l_line[0]),int(l_line[1])
					# print(self.sizeH,self.sizeV)
				elif lineNumber == 2:
					self.nWallSquares,self.wallCoordinates = int(l_line[0]),self.string_to_int_list(l_line[1: ])
					self.wallCoordinates = self.group_coordinates(self.nWallSquares,self.wallCoordinates)
					# print(self.nWallSquares,self.wallCoordinates)
				elif lineNumber == 3:
					self.nBoxes,self.boxCoordinates = int(l_line[0]),self.string_to_int_list(l_line[1: ])
					self.boxCoordinates = self.group_coordinates(self.nBoxes,self.boxCoordinates)
				elif lineNumber == 4:
					self.nstorLocations,self.storCoordinates = int(l_line[0]),self.string_to_int_list(l_line[1: ])
					self.storCoordinates = self.group_coordinates(self.nstorLocations,self.storCoordinates)
				elif lineNumber == 5:
					# -1 to match python array indices
					self.playerLoc = (int(l_line[0])-1,int(l_line[1])-1) # (x,y) tuple
				lineNumber += 1

	"""While game playing, sizeH, sizeV, nWallSquares, wallCoordinates, nBoxes, nstorLocations, storCoordinates
	remains fixed. The two variables which change according to the input are boxCordinates and playerLoc."""

	def box_on_goal(self):
		# check if any of the boxes are on any of the storage locations
		flag = [i for i in self.boxCoordinates if i in self.storCoordinates]
		if len(flag) > 0:
			return (True, flag)
		return False

	def sokoban_on_goal(self):
		# check if Sokoban is on goal
		if self.playerLoc in self.storCoordinates:
			return True
		return False

	def is_goal_state(self):
		return sorted(self.storCoordinates) == sorted(self.boxCoordinates)

	def make_board_grid(self):
		if self.sizeH is None or self.sizeV is None:
			return False
		# self.sizeV is the number of lists in self.boardGrid and self.sizeH is the size of each list
		self.boardGrid = [[' ' for i in range(self.sizeH)] for j in range(self.sizeV)]

		for i in range(self.nWallSquares):
			self.boardGrid[self.wallCoordinates[i][0]][self.wallCoordinates[i][1]] = '#'

		for i in range(self.nstorLocations):
			self.boardGrid[self.storCoordinates[i][0]][self.storCoordinates[i][1]] = '.'

		for i in range(self.nBoxes):
			self.boardGrid[self.boxCoordinates[i][0]][self.boxCoordinates[i][1]] = '$'

		# check if any of the boxes are on any of the storage locations
		result = self.box_on_goal()
		if result:
			stored_coordinates = result[1]
			# print(stored_coordinates, '@'*10)
			for i in range(len(stored_coordinates)):
				self.boardGrid[stored_coordinates[i][0]][stored_coordinates[i][1]] = '*'

		# check if Sokoban is on goal
		if self.sokoban_on_goal():
			# print('sokoban on gloal')
			self.boardGrid[self.playerLoc[0]][self.playerLoc[1]] = '+'
		else:
			# print('sokoban not on goal')
			self.boardGrid[self.playerLoc[0]][self.playerLoc[1]] = '@'

		return self.boardGrid

	def display_board(self):
		"""
		"#" - Wall
		" " - Free Space
		"$" - Box
		"." - Goal Place
		"*" - Box is placed on a goal
		"@" - Sokoban
		"+" - Sokoban on a goal
		"""
		for i in range(self.sizeV):
			for j in range(self.sizeH):
				print(self.boardGrid[i][j], end = '')
			print('')

	def is_legal_move(self, action): 
		x, y = None, None
		if action.isupper():
			# print('isupper')
			x, y = self.playerLoc[0] + 2*self.actions[action][0], self.playerLoc[1] + 2*self.actions[action][1] # look two steps ahead
		else:
			# print('islower')
			# print('test')
			x, y = self.playerLoc[0] + self.actions[action][0], self.playerLoc[1] + self.actions[action][1] # look one step ahead

		"""If there is not box next to the Sokobon and the input is still uppercase, then we can expect funny behavior from this code"""
		coord = (x,y)
		# print(coord, 'FLAG**')
		# print(self.wallCoordinates)
		if (coord in self.boxCoordinates) or (coord in self.wallCoordinates):
			# print('1')
			coord = False
		if x<0 or x>self.sizeV - 1:
			# print('2')
			coord = False
		if y<0 or y>self.sizeH - 1:
			# print('3')
			coord = False
		# print(coord, 'FLAG##')
		return coord

	# if move is legal then update board
	def update_board(self, action): 
		# print(self.is_legal_move(action), '?IS LEGAL?')
		if self.is_legal_move(action):
			# print(self.playerLoc, 'OLD PLAYER LOCATION')
			(x,y) = (self.playerLoc[0]+self.actions[action][0], self.playerLoc[1]+self.actions[action][1])
			# print(self.playerLoc)
			# print(x,y)
			if action.isupper() and (x,y) in self.boxCoordinates:
				# print(self.boxCoordinates)
				self.boxCoordinates.remove((x,y))
				self.boxCoordinates.append((self.playerLoc[0]+2*self.actions[action][0], self.playerLoc[1]+2*self.actions[action][1]))
				# print(self.boxCoordinates)
			self.playerLoc = (x,y)
			return True
		return False

	# def pseudo_update_board(self, action):
		# assert self.is_legal_move(action)
		# (x, y) = (self.playerLoc[0]+self.actions[action][0], self.playerLoc[1]+self.actions[action][1])
		# both box and player coordinates change
		# if action.isupper() and (x,y) in self.boxCoordinates:
			# newBoxCoordinates = deepcopy(self.boxCoordinates)
			# newBoxCoordinates.remove((x, y))
			# newBoxCoordinates.append((self.playerLoc[0]+2*self.actions[action][0], self.playerLoc[1]+2*self.actions[action][1]))
		# else:
			# newBoxCoordinates = deepcopy(self.boxCoordinates)
		# newPlayerCoordinates = deepcopy((x, y))
		# return newPlayerCoordinates, newBoxCoordinates

	def possible_moves(self):
		legal_actions = []
		for action in self.actions:
			if self.is_legal_move(action):
				(x,y) = (self.playerLoc[0]+self.actions[action][0], self.playerLoc[1]+self.actions[action][1])
				if (x,y) in self.boxCoordinates and action.islower():
					continue
				if (x,y) not in self.boxCoordinates and action.isupper():
					continue
				legal_actions.append(action)
		return legal_actions

class PriorityQueue:
    def  __init__(self):
        self.Heap = []
        self.Count = 0

    def push(self, item, priority):
        entry = (priority, self.Count, item) 
        heapq.heappush(self.Heap, entry) 
        self.Count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.Heap) # heapq is a minheap so node with lowest priority/(heutistic+cost) will be popped first
        return item

class Heuristic:
	def __init__(self):
		self.name = None

	def set_heuristic(self, name):
		self.name = name

	def calculate(self, storCoordinates, boxCoordinates):
		heuristicVal = 0
		if self.name == "manhattan" or self.name == None:
			for box in boxCoordinates:
				for storage in storCoordinates:
					heuristicVal += (abs(storage[0] - box[0])+abs(storage[1] - box[1])) # WHAT THE HECK DO storage() AND box() RETURN? 
		elif self.name == "euclidean":
			for box in boxCoordinates:
				for storage in storCoordinates:
					heuristicVal += sqrt((abs(storage[0] - box[0])^2+abs(storage[1] - box[1])^2))

		return heuristicVal

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

def main():
	print("Enter sokoban board file number (example: 01) from input_files folder: ")
	number = input()
	print('-'*20)
	boardInputFile = os.path.join(os.getcwd(), 'input_files', 'sokoban'+str(number)+'.txt')
	assert os.path.isfile(boardInputFile)
	sokobanBoard = Board(boardInputFile)
	game = Game(sokobanBoard)
	print('-'*20)
	# game.play_moves(['r', 'r', 'd', 'd', 'd', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'u', 'L',
	 # 'L', 'L', 'L', 'L', 'L', 'L', 'L', 'u', 'l', 'D', 'D', 'D', 'D', 'r', 'd', 'L'])
	print(game.play_AStar())
	# moves = list('rDlddrrruuLLrrddllUdrruulullDRddl')
	# print(len(moves))
	# game.play_moves(moves)


main()
