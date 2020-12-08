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