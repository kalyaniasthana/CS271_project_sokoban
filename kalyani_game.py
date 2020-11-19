import os # will mostly use this to NOT hard code paths

#I think it's a good idea to use an OOP approach for this project
class board:

	#initialise board variables 

	def __init__(self, board_input_file):
		self.sizeH, self.sizeV, self.nWallSquares, self.wallCoordinates, self.nBoxes, \
		self.boxCoordinates, self.nstorLocations, self.storCoordinates, self.playerLoc = \
		None, None, None, None, None, None, None, None, None
		self.board_input_file, self.board_grid = board_input_file, None

	#parse input file - sokobanXY.txt

	def __str__(self):
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

	def parse(self):

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
		flag = [i for i in self.boxCoordinates if i in self.storCoordinates]
		if len(flag) > 0:
			return (True, flag)
		return False

	def sokoban_on_goal(self):
		if self.playerLoc in self.storCoordinates:
			return True
		return False

	def make_board_grid(self):
		if self.sizeH is None or self.sizeV is None:
			return 'Error: Game Board in not initialised!'
		#self.sizeV is the number of lists in self.board_grid and self.sizeH is the size of each list
		self.board_grid = [[' ' for i in range(self.sizeH)] for j in range(self.sizeV)]

		#check if Sokoban is on goal
		if self.sokoban_on_goal():
			self.board_gridboard_grid[self.playerLoc[0]][self.playerLoc[1]] = '+'
		else:
			self.board_grid[self.playerLoc[0]][self.playerLoc[1]] = '@'

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

def main():
	board_input_file = os.path.join(os.getcwd(), 'input_files', 'sokoban00.txt')
	sokoban_board = board(board_input_file)
	sokoban_board.parse()
	sokoban_board.make_board_grid()
	sokoban_board.display_board()
	print(sokoban_board)

main()
