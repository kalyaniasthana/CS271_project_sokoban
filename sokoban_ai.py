import os # will mostly use this to NOT hard code paths

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
		return self.SizeV

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
			for i in range(len(stored_coordinates)):
				self.boardGrid[self.boxCoordinates[i][0]][self.boxCoordinates[i][1]] = '*'

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
			#print('1')
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
        (_, _, item) = heapq.heappop(self.Heap)
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
					heuristicVal += (abs(storage(1) - box(1))+abs(storage(2) - box(2))) # WHAT DO storage() AND box() RETURN? 
		elif self.name == "euclidean":
			for box in boxCoordinates:
				for storage in storCoordinates:
					heuristicVal += sqrt((abs(storage(1) - box(1))^2+abs(storage(2) - box(2))^2))

		return heuristicVal

class Game:
	def __init__(self, board):
		self.board = board
		self.board.parse()
		self.board.make_board_grid()
		self.board.display_board()
		# print(sokoban_board)
		# print('-'*20)

	def play_moves(self, moves):
		# moves = ['l', 'u', 'U', 'U', 'U']
		if moves:
			for move in moves:
				if self.board.update_board(move):
					self.board.make_board_grid()
					self.board.display_board()
					# print(sokoban_board)
					print('-'*20)
					print(self.board.possible_moves(), "POSSIBLE MOVES")
				else:
					print("COULD NOT UPDATE BOARD")
				if self.board.is_goal_state():
					print("GOAL STATE!")
					break

	def play_AStar(self):
		"""Implement A* search"""
		def cost(actions): return len([x for x in actions if x.islower()]) # defining cost to be uniformly 1 for non-pushes

		# these are (almost) the same as in BFS
		boxCoordinates = self.board.get_box_coordinates()
		player = self.board.get_player_loc()
		storCoordinates = self.board.get_stor_coordinates()
		starting = (player, boxCoordinates)
		visited = set()

		# implementing frontier and actions as priority queues
		frontier = PriorityQueue()
		actions = PriorityQueue()

		H = Heuristic()
		heuristicVal = H.calculate(storCoordinates, boxCoordinates)

		frontier.push([starting], heuristicVal)
		actions.push([0], heuristicVal)

		while frontier:
			node = frontier.pop()
			nodeAction = actions.pop()
			# check if we are in a goal state, before proceeding to search
			if self.board.is_goal_state():
				return(','.join(nodeAction[1:]).replace(',',''))

			if node[-1] not in visited:
				visited.add(node[-1])
				Cost = cost(nodeAction[1:])

				for action in possibleMoves(node[-1][0], node[-1][1]):
					self.board.update_board(action)

				if self.isDeadEnd():
					continue

				newPlayer = self.board.get_player_loc()
				newBoxCoordinates = self.board.get_box_coordinates() # get the new box coordinates here to feed to Heuristic
				heuristicVal = H.calculate(storCoordinates, newBoxCoordinates)

				frontier.push(node + [(newPlayer, newBoxCoordinates)], Cost + heuristicVal) # priority value f(n) = cost-to-current-node + heuristic-of-current-node
				actions.push(nodeAction + [action[-1]], Cost + heuristicVal)


	def corner_deadlock(self):
		boardGrid = self.board.get_board_grid()
		h = self.board.get_sizeH()
		v = self.board.get_sizeV()
		boxes = self.board.get_box_coordinates()
		for coord in boxes:
			i = coord(1)
			j = coord(2)
			if (boardGrid[i-1][j] == '#' and boardGrid[i][j-1] == '#'):
				return True
			elif (boardGrid[i+1][j] == '#' and boardGrid[i][j-1] == '#'):
				return True
			elif (boardGrid[i][j+1] == '#' and boardGrid[i-1][j] == '#'):
				return True
			elif (boardGrid[i][j+1] == '#' and boardGrid[i+1][j] == '#'):
				return True
		return False

	def pre_corner_deadlock(self):
		"""It's one of these cases (same vertically):

			#      $                #     ##################...###
			 ##################...###     #          $           #
			 And there is no goal on the axis
		"""
		boardGrid = self.board.get_board_grid()
		h = self.board.get_sizeH()
		v = self.board.get_sizeV()
		boxes = self.board.get_box_coordinates()
		storages = self.board.get_stor_coordinates()
		for coord in boxes:
			i = coord(1)
			j = coord(2)
			if j == 1 or j == (h-2):
				for store in storages:
					if store(2) == 1 or store(2) == (v-2):
						if store(1) >= 1 or store(1) <= (h-2):
							return False
					else:
						# It means that there is no store location but there is a box
						return True
			elif i == 1 or i == (v-2):
				for store in storages:
					if store(1) == 1 or store(1) == (h-2):
						if store(2) >= 1 or store(2) <= (v-2):
							return False
					else:
						# It means that there is no store location but there is a box
						return True
		return False

	def square_block_deadend(self):
		boardGrid = self.board.get_board_grid()
		h = self.board.get_sizeH()
		v = self.board.get_sizeV()
		for i in range(h-1):
			for j in range(v-1):
				if self.square_block_checker(i, j, boardGrid):
					return True

	def square_block_checker(self, i, j, boardGrid):
		if boardGrid[i+1][j] == '$':
			return self.box_block_deadend(i+1, j)
		elif boardGrid[i][j+1] == '$':
			return self.box_block_deadend(i, j+1)
		elif boardGrid[i-1][j] == '$' and boardGrid[i][j-1] == '$':
			return True
		return False


	def isDeadEnd(self):
		if self.simple_deadlock() or self.pre_corner_deadlock() or self.square_block_deadend() :
			return True
		return False

	# def playBFS(self):
	# 	boxes = self.board.get_box_coordinates()
	# 	player = self.board.get_player_loc()
	# 	starting = (player, boxes) # a tuple, left-hand-side is player position, right-hand-side is box coordinates
	# 	frontier = collections.deque([[starting]]) # creates a search frontier
	# 	actions = collections.deque([[0]])
	# 	visited = set()
	# 	while frontier:
	# 		node = frontier.popleft()
	# 		node_action = actions.popleft()
	# 		if goalCheck(node[-1][-1]):
	# 			print(','.join(node_action[1:]).replace(',',''))
	# 			break
	# 		if node[-1] not in visited:
	# 			visited.add(node[-1])
	# 			for action in self.board.possible_moves():
	# 				newPlayer, newBoxes = updateBoard(node[-1][0], node[-1][1], action)
	# 				# if deadEndCheck(newBoxes):
	# 				# have to think about what to check for dead ends
	# 				#     continue
	# 				frontier.append(node + [(newPlayer, newBoxes)])
	# 				actions.append(node_action + [action[-1]])

	# 	print("Success!")



def main():
	print("Introduce sokoban file number (example: 01) in input_files folder:")
	number = input()
	boardInputFile = os.path.join(os.getcwd(), 'input_files', 'sokoban'+str(number)+'.txt')
	board = Board(boardInputFile)
	game = 	Game(board)
	print("Introduce the Agent you want to try:\n[1] No Agent\n[2] BFS\n[3] A* Star Search")
	number = int(input())

	if number == 1:
		print("case 1")
		game.play()
	elif number == 2:
		game.playBFS()
	elif number == 3:
		print("Introduce the Heuristic you want to try:\n[1] Manhattan Distance\n[2] Euclidean Distance\n[3] Mongolian Algorithm")
		number2 = int(input())
		if number2 == 1:
			heuristic = game.manhattan_heuristic()
			game.play_AStar(heuristic)
		elif number2 == 2:
			heuristic = game.euclidean_heuristic()
			game.play_AStar(heuristic)
		elif number2 == 3:
			heuristic = game.mongolian_heuristic()
			game.play_AStar(heuristic)
		else:
			print("Wrong heuristic")
	else:
		print("Wrong number")



main()
