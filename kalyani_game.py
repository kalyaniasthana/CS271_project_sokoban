import os # will mostly use this to NOT hard code paths
import collections 

'''
How do we modify our code to incorporate numpy arrays and scipy sparse matrices into it
and make it both more space and memory efficient? 
If we go ahead with this modification, we might have to rewrite more than 60% of this script.
I really don't mind though. I'm pretty sure we don't need so many class variables. 
Instead, use a character numpy array. numpy arrays have optimized find functions. 
I guess SciPy array have similar optimized functions and will save a lot of memory on top of that. 
The possible approach in my head sounds like a classic memory vs speed tradeoff.
'''

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

	#seems like I suck at inheritance since I've made only one class till now
'''
	def BFS(self):
		return None
		#input: start state
		#output: series of actions from start state to goal state
		player = (self.playerLoc[0], self.playerLoc[1])
		start_state = (player, self.boxCoordinates) # each state is a tuple with the player's location and the box coordinates

		frontier = [[start_state]]
		paths = [['']]
		visited = []
		#visited.append(start_state)

		while frontier:
			current_state = frontier.pop(0)
			current_path = paths.pop(0)
			if self.is_goal_state():
				return current_path
			if current_state[-1] not in visited:
				visited.append(current_state[-1])
				for action in self.possible_moves():
					self.update_board(action)
					new_player = (self.playerLoc[0], self.playerLoc[1])
					
					if self.is_dead_end(): 
						continue
					
					frontier.append(current_state + [(new_player, self.boxCoordinates)])
					paths.append(current_path + [action[-1]])
'''   

'''
	def aStarSearch(self):

		def cost(node_action):
			return len([x for x in actions if x.islower()])

		#we don't need to get_player and get_boxes since this function can access 'self' for that
		player = (self.playerLoc[0], self.playerLoc[1])
		start_state = (player, self.boxCoordinates)

		visited = []
		frontier = PriorityQueue()
		actions = PriorityQueue()

		while frontier:
			node = frontier.pop()
			node_action = actions.pop()
			if self.is_goal_state():
				return ','.join(node_action[1:]).replace(',','')
			if node[-1] not in visited:
				visited.append(node[-1])
				Cost = cost(node_action[1:]) #need to define a cost function. Simplest way is to have
				# 'actions' should look like the list 'moves' in the main() function
				for action in self.possible_moves():
					self.update_board(action)
					new_player = (self.playerLoc[0], self.playerLoc[1])
					if self.is_dead_end():
						continue
					Heuristic = self.heuristic()
					frontier.push(node + [(new_player, self.boxCoordinates)], Heuristic + Cost) 
					actions.push(node_action + [action[-1]], Heuristic + Cost)
'''        

def main():
	board_input_file = os.path.join(os.getcwd(), 'input_files', 'sokoban01.txt')
	sokoban_board = Board(board_input_file)
	sokoban_board.parse()
	sokoban_board.make_board_grid()
	sokoban_board.display_board()
	#print(sokoban_board)
	print('-'*20)
	'''
	print(sokoban_board.possible_moves(), 'POSSIBLE MOVES')
	
	moves = ['l', 'u', 'U', 'U', 'U']
	if moves:
		for move in moves:
			if sokoban_board.update_board(move):
				sokoban_board.make_board_grid()
				sokoban_board.display_board()
				#print(sokoban_board)
				print('-'*20)
				print(sokoban_board.possible_moves(), 'POSSIBLE MOVES')
			else:
				print('COULD NOT UPDATE BOARD')
			if sokoban_board.is_goal_state():
				print('GOAL STATE!')
				break
			#break
	'''
	print(sokoban_board.BFS())


main()
