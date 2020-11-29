import os

class Sokoban_Generator:

    def __init__(self, board_input_file, number):
        #initialise board variables
        self.sizeH, self.sizeV, self.nWallSquares, self.wallCoordinates, self.nBoxes, \
        self.boxCoordinates, self.nstorLocations, self.storCoordinates, self.playerLoc = \
        0, 0, 0, [], 0, [], 0, [], ()
        self.board_input_file = board_input_file
        self.number = number

    def parse(self): #parse input file - inputXY.txt to sokobanXY.txt

        """Explanation ...."""
        with open(self.board_input_file) as f:
            i = 0
            for line in f:
                if i == 0:
                    l_line = line.split(' ')
                    self.sizeH = int(l_line[0])
                    self.sizeV = int(l_line[1])
                else:
                    for j in range(self.sizeH):
                        char = line[j]
                        self.adder(char, j, i)
                i += 1

        self.writing_on_file()

    def adder(self, char, i, j): #converts a square in inputXY depending on its content
        if char == '@':
            self.playerLoc = (i, j)
        elif char == '#':
            self.nWallSquares += 1
            self.wallCoordinates.append((i,j))
        elif char == '$':
            self.nBoxes += 1
            self.boxCoordinates.append((i,j))
        elif char == '.':
            self.nstorLocations += 1
            self.storCoordinates.append((i,j))


import os # will mostly use this to NOT hard code paths

#I think it's a good idea to use an OOP approach for this project
class Board:

	def __init__(self, board_input_file):
		#initialise board variables
		self.sizeH, self.sizeV, self.nWallSquares, self.wallCoordinates, self.nBoxes, \
		self.boxCoordinates, self.nstorLocations, self.storCoordinates, self.playerLoc = \
		None, None, None, None, None, None, None, None, None
		self.board_input_file, self.board_grid = board_input_file, None
		self.actions = {'u': (-1,0), 'U': (-1,0), 'l': (0,-1), 'L': (0,-1), 'd': (1,0), 'D': (1,0), 'r': (0,1), 'R': (0,1)}

	def __str__(self):
		'''display class variables'''
		return 'sizeH: {self.sizeH}, sizeV: {self.sizeV}, nWallSquares: {self.nWallSquares}, wallCoordinates: {self.wallCoordinates}, nBoxes: {self.nBoxes}, boxCooridates: {self.boxCoordinates}, nstorLocations: {self.nstorLocations}, storCoordinates: {self.storCoordinates}, playerLoc: {self.playerLoc}'.format(self = self)

	def string_to_int_list(self, string_list):
		return list(map(int, string_list))

	def group_coordinates(self, n, coord_list):
		''' new_coord_list is a list of tuples. I think it's a good idea to use tuples for positions in the game board.
		The initial position of sokoban is also a tuple (x,y)'''
		new_coord_list = []
		for i in range(0, n*2, 2):
			# -1 to match python array indices
			new_coord_list.append((coord_list[i] - 1, coord_list[i+1] - 1))
		return new_coord_list

	def parse(self): #parse input file - sokobanXY.txt

		'''input is expected to have 5 lines
		line 1 is the sizeH, sizeV
		line 2 is nWallSquares followed by a list wallCoordinates
		line 3 is a list of boxCordinates
		line 4 is a list of storCoordinates (storage location coordinates)
		line 5 is the initial position of SOKOBAN'''

		line_number = 1 # to iterate through the lines
		with open(self.board_input_file) as f:
			for line in f:

				l_line = line.split(' ')

				if line_number == 1:
					self.sizeH, self.sizeV = int(l_line[0]),int(l_line[1])
					#print(self.sizeH,self.sizeV)
				elif line_number == 2:
					self.nWallSquares,self.wallCoordinates = int(l_line[0]),self.string_to_int_list(l_line[1: ])
					self.wallCoordinates = self.group_coordinates(self.nWallSquares,self.wallCoordinates)
					#print(self.nWallSquares,self.wallCoordinates)
				elif line_number == 3:
					self.nBoxes,self.boxCoordinates = int(l_line[0]),self.string_to_int_list(l_line[1: ])
					self.boxCoordinates = self.group_coordinates(self.nBoxes,self.boxCoordinates)
				elif line_number == 4:
					self.nstorLocations,self.storCoordinates = int(l_line[0]),self.string_to_int_list(l_line[1: ])
					self.storCoordinates = self.group_coordinates(self.nstorLocations,self.storCoordinates)
				elif line_number == 5:
					#-1 to match python array indices
					self.playerLoc = (int(l_line[0])-1,int(l_line[1])-1) #(x,y) tuple
				line_number += 1

	'''while game playing, sizeH, sizeV, nWallSquares, wallCoordinates, nBoxes, nstorLocations, storCoordinates
	remains fixed. The two variables which change according to the input are boxCordinates and playerLoc.
	'''


	def getSizeH(self):
		return self.sizeH

	def getSizeV(self):
		return self.SizeV

	def getNWallSquares(self):
		return self.nWallSquares

	def getwallCoordinates(self):
		return self.wallCoordinates

	def getNBoxes(self):
		return self.nBoxes

	def getBoxCoordinates(self):
		return self.boxCoordinates

	def getNStorLocations(self):
		return self.nstorLocations

	def getStorCoordiantes(self):
		return self.storCoordinates

	def getPlayerLoc(self):
		return self.playerLoc

	def getBoardGrid(self):
		return self.board_grid


	def box_on_goal(self):
		#check if any of the boxes are on any of the storage locations
		flag = [i for i in self.boxCoordinates if i in self.storCoordinates]
		if len(flag) > 0:
			return (True, flag)
		return False

	def sokoban_on_goal(self):
		#check if Sokoban is on goal
		if self.playerLoc in self.storCoordinates:
			return True
		return False

	def is_goal_state(self):
		return sorted(self.storCoordinates) == sorted(self.boxCoordinates)

	def make_board_grid(self):
		if self.sizeH is None or self.sizeV is None:
			return False
		#self.sizeV is the number of lists in self.board_grid and self.sizeH is the size of each list
		self.board_grid = [[' ' for i in range(self.sizeH)] for j in range(self.sizeV)]

		for i in range(self.nWallSquares):
			self.board_grid[self.wallCoordinates[i][0]][self.wallCoordinates[i][1]] = '#'

		for i in range(self.nstorLocations):
			self.board_grid[self.storCoordinates[i][0]][self.storCoordinates[i][1]] = '.'

		for i in range(self.nBoxes):
			self.board_grid[self.boxCoordinates[i][0]][self.boxCoordinates[i][1]] = '$'

		#check if any of the boxes are on any of the storage locations
		result = self.box_on_goal()
		if result:
			stored_coordinates = result[1]
			for i in range(len(stored_coordinates)):
				self.board_grid[self.boxCoordinates[i][0]][self.boxCoordinates[i][1]] = '*'

		#check if Sokoban is on goal

		if self.sokoban_on_goal():
			#print('sokoban on gloal')
			self.board_grid[self.playerLoc[0]][self.playerLoc[1]] = '+'
		else:
			#print('sokoban not on goal')
			self.board_grid[self.playerLoc[0]][self.playerLoc[1]] = '@'

		return self.board_grid

	def display_board(self):
		'''
		"#" - Wall
		" " - Free Space
		"$" - Box
		"." - Goal Place
		"*" - Box is placed on a goal
		"@" - Sokoban
		"+" - Sokoban on a goal
		'''
		for i in range(self.sizeV):
			for j in range(self.sizeH):
				print(self.board_grid[i][j], end = '')
			print('')

	#TODO: functions: check_legal_move(), update_board_variables()
	#Should I create a new class for moving the Sokoban?
	#The lowercase letters “uldr” are used for moves and the uppercase letters “ULDR” for pushes.

	'''this function breaks when the game expects a lowercase input but the input is uppercase and vice-versa'''
	def is_legal_move(self, action): #same as Jason's implementation of this function
		x, y = None, None
		if action.isupper():
			#print('isupper')
			x, y = self.playerLoc[0] + 2*self.actions[action][0], self.playerLoc[1] + 2*self.actions[action][1] #look two steps ahead
		else:
			#print('islower')
			#print('test')
			x, y = self.playerLoc[0] + self.actions[action][0], self.playerLoc[1] + self.actions[action][1] #look one step ahead

		'''If there is not box next to the Sokobon and the input is still uppercase, then we can expect funny behavior from this code'''
		coord = (x,y)
		#print(coord, 'FLAG**')
		#print(self.wallCoordinates)
		if (coord in self.boxCoordinates) or (coord in self.wallCoordinates):
			#print('1')
			coord = False
		if x<0 or x>self.sizeV - 1:
			#print('2')
			coord = False
		if y<0 or y>self.sizeH - 1:
			#print('3')
			coord = False
		#print(coord, 'FLAG##')
		return coord

	#if move is legal then update board
	def update_board(self, action): #also the same as Jason's implementation

		print(self.is_legal_move(action), '?IS LEGAL?')
		if self.is_legal_move(action):
			#print(self.playerLoc, 'OLD PLAYER LOCATION')
			(x,y) = (self.playerLoc[0]+self.actions[action][0], self.playerLoc[1]+self.actions[action][1])
			#print(self.playerLoc)
			#print(x,y)
			if action.isupper() and (x,y) in self.boxCoordinates:
				#print(self.boxCoordinates)
				self.boxCoordinates.remove((x,y))
				self.boxCoordinates.append((self.playerLoc[0]+2*self.actions[action][0], self.playerLoc[1]+2*self.actions[action][1]))
				#print(self.boxCoordinates)
			self.playerLoc = (x,y)
			return True
		return False

	def possible_moves(self):
		'''
		directions = {(-1,0): ['u', 'U'], (0,-1): ['l', 'L'], (1,0): ['d', 'D'], (0,1): ['r', 'R']}
		legal_actions = []
		for direction in directions:
			if self.is_legal_move(directions[direction][0]):
				if (self.playerLoc[0]+direction[0], self.playerLoc[1]+direction[1]) in self.boxCoordinates:
					legal_actions.append(directions[direction][1])
				else:
					legal_actions.append(directions[direction][0])
			if self.is_legal_move(directions[direction][1]):
				legal_actions.append(directions[direction][1])
		return legal_actions
		'''
		legal_actions = []
		for action in self.actions:
			if self.is_legal_move(action):
				(x,y) = (self.playerLoc[0]+self.actions[action][0],self.playerLoc[1]+self.actions[action][1])
				if (x,y) in self.boxCoordinates and action.islower():
					continue
				if (x,y) not in self.boxCoordinates and action.isupper():
					continue
				legal_actions.append(action)
		return legal_actions

class PriorityQueue:
    """Define a PriorityQueue data structure that will be used"""
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

	def setHeuristic(self, name):
		self.name = name

	def calculate(self, storages, boxes):
		heuristics_val = 0
		if self.name == "manhattan" or self.name == None:
			for box in boxes:
				for storage in storages:
					heuristics_val += (abs(storage(1) - box(1))+ abs(storage(2) - box(2)))
		elif self.name == "euclidean":
			for box in boxes:
				for storage in storages:
					heuristics_val += sqrt((abs(storage(1) - box(1))^2+ abs(storage(2) - box(2))^2))

		return heuristics_val

class Game:
	def __init__(self, board):
		self.board = board
		self.board.parse()
		self.board.make_board_grid()
		self.board.display_board()
		#print(sokoban_board)
		print('-'*20)

	def play(self):
		moves = ['l', 'u', 'U', 'U', 'U']
		if moves:
			for move in moves:
				if self.board.update_board(move):
					self.board.make_board_grid()
					self.board.display_board()
					#print(sokoban_board)
					print('-'*20)
					print(self.board.possible_moves(), 'POSSIBLE MOVES')
				else:
					print('COULD NOT UPDATE BOARD')
				if self.board.is_goal_state():
					print('GOAL STATE!')
					break
					#break


	def playAStar(self):
		"""Implement A* search"""
		def cost(actions): return len([x for x in actions if x.islower()]) # defining cost to be uniformly 1 for non-pushes

		# these are (almost) the same as in BFS
		boxes = self.board.getBoxCoordinates()
		player = self.board.getPlayerLoc()
		storage = self.board.getStorCoordiantes()
		starting = (player, boxes)
		visited = set()

		# implementing frontier and actions as priority queues.
		frontier = PriorityQueue()
		actions = PriorityQueue()

		h = Heuristic()
		heur = h.calculate(storage, boxes)

		frontier.push([starting], heur)
		actions.push([0], heur)

		while frontier:
			node = frontier.pop()
			node_action = actions.pop()
			# check if we are in a goal state, before proceeding to search
			if self.board.is_goal_state():
				return(','.join(node_action[1:]).replace(',',''))

			if node[-1] not in visited:
				visited.add(node[-1])
				Cost = cost(node_action[1:])

				for action in possibleMoves(node[-1][0], node[-1][1]):
					self.board.update_board(action)

				if self.isDeadEnd():
					continue

				newPlayer = self.board.getPlayerLoc()
				newBoxes = self.board.getBoxCoordinates() # get the new box coordinates here to feed to Heuristic
				heur = h.calculate(storage, newBoxes)

				frontier.push(node + [(newPlayer, newBoxes)], Cost + heur) # priority value f(n) = cost-to-current-node + heuristic-of-current-node
				actions.push(node_action + [action[-1]], Cost + heur)


	def corner_deadlock(self):
		board_grid = self.board.getBoardGrid()
		h = self.board.getSizeH()
		v = self.board.getSizeV()
		boxes = self.board.getBoxCoordinates()
		for coord in boxes:
			i = coord(1)
			j = coord(2)
			if (board_grid[i-1][j] == '#' and board_grid[i][j-1] == '#'):
				return True
			elif (board_grid[i+1][j] == '#' and board_grid[i][j-1] == '#'):
				return True
			elif (board_grid[i][j+1] == '#' and board_grid[i-1][j] == '#'):
				return True
			elif (board_grid[i][j+1] == '#' and board_grid[i+1][j] == '#'):
				return True
		return False

	def pre_corner_deadlock(self):
		"""It's one of these cases (same vertically):

			#      $                #     ##################...###
			 ##################...###     #          $           #
			 And there is no goal on the axis
		"""
		board_grid = self.board.getBoardGrid()
		h = self.board.getSizeH()
		v = self.board.getSizeV()
		boxes = self.board.getBoxCoordinates()
		storages = self.board.getStorCoordiantes()
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
		board_grid = self.board.getBoardGrid()
		h = self.board.getSizeH()
		v = self.board.getSizeV()
		for i in range(h-1):
			for j in range(v-1):
				if self.square_block_checker(i, j, board_grid):
					return True

	def square_block_checker(self, i, j, board_grid):
		if board_grid[i+1][j] == '$':
			return self.box_block_deadend(i+1, j)
		elif board_grid[i][j+1] == '$':
			return self.box_block_deadend(i, j+1)
		elif board_grid[i-1][j] == '$' and board_grid[i][j-1] == '$':
			return True
		return False


	def isDeadEnd(self):
		if self.simple_deadlock() or self.pre_corner_deadlock() or self.square_block_deadend() :
			return True
		return False

	# def playBFS(self):
	# 	boxes = self.board.getBoxCoordinates()
	# 	player = self.board.getPlayerLoc()
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
	print("Introduce number of sokoban file (example: 01) in input_files folder:")
	number = input()
	board_input_file = os.path.join(os.getcwd(), 'input_files', 'sokoban'+str(number)+'.txt')
	board = Board(board_input_file)
	game = 	Game(board)
	print("Introduce Agent you want to try:\n[1] No Agent\n[2] BFS\n[3] A* Star Search")
	number = int(input())

	if number == 1:
		print("case 1")
		game.play()
	elif number == 2:
		game.playBFS()
	elif number == 3:
		print("Introduce Case you want to try:\n[1] Manhattan Distance\n[2] Euclidean Distance\n[3] Mongolian Algorithm")
		number2 = int(input())
		if number2 == 1:
			heuristic = game.manhattan_heuristic()
			game.playAStar(heuristic)
		elif number2 == 2:
			heuristic = game.euclidean_heuristic()
			game.playAStar(heuristic)
		elif number2 == 3:
			heuristic = game.mongolian_heuristic()
			game.playAStar(heuristic)
		else:
			print("Wrong heuristic")
	else:
		print("Wrong number")



main()

    def writing_on_file(self):
        path = os.path.join(os.getcwd(), 'input_files', "sokoban"+self.number+".txt")
        with open(path, "a") as f2:
            for i in range(4):
                if i == 0:
                    # Line 1 is the sizeH, sizeV
                    f2.write(str(self.sizeH)+" "+str(self.sizeV))
                    f2.write("\n") #add the breakline
                elif i == 1:
                    f2.write(str(self.nWallSquares))
                    # Line 2 is the number of walls and the list of coordinates
                    for k in self.wallCoordinates:
                        f2.write(" "+str(k[0])+" "+str(k[1]))
                    f2.write("\n") #add the breakline
                elif i == 2:
                    # Line 3 is the number of boxes and the list of coordinates
                    f2.write(str(self.nBoxes))
                    # Line 2 is the number of walls and the list of coordinates
                    for k in self.boxCoordinates:
                        f2.write(" "+str(k[0])+" "+str(k[1]))

                    f2.write("\n") #add the breakline
                elif i == 3:
                    # Line 4 is the number of storage places and its coordinates
                    f2.write(str(self.nstorLocations))
                    # Line 2 is the number of walls and the list of coordinates
                    for k in self.storCoordinates:
                        f2.write(" "+str(k[0])+" "+str(k[1]))

                    f2.write("\n") #add the breakline
                elif i == 4:
                    # Line 5 is the initial position of player
                    f2.write(str(self.playerLoc[0])+" "+str(self.playerLoc[1]))

def main():
    print("Introduce number of inputXY.txt you want to generate as sokobanXY.txt (example 01)")
    str_number = str(input())
    board_input_file = os.path.join(os.getcwd(), 'input_files', 'input'+str_number+'.txt')
    sokoban_board = Sokoban_Generator(board_input_file, str_number)
    sokoban_board.parse()


main()
