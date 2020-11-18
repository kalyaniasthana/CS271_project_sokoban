import os # will mostly use this to NOT hard code paths

#I think it's a good idea to use an OOP approach for this project
class board:

	#initialise board variables 

	def __init__(self, board_input_file):
		self.sizeH, self.sizeV, self.nWallSquares, self.wallCoordinates, self.nBoxes, \
		self.boxCoordinates, self.nstorLocations, self.storCoordinates, self.playerLoc = \
		None, None, None, None, None, None, None, None, None
		self.board_input_file = board_input_file

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
			new_coord_list.append((coord_list[i], coord_list[i+1]))
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
					self.playerLoc = (int(l_line[0]),int(l_line[1])) #(x,y) tuple
				line_number += 1

def main():
	board_input_file = os.path.join(os.getcwd(), 'input_files', 'sokoban01.txt')
	sokoban_board = board(board_input_file)
	sokoban_board.parse()
	print(sokoban_board)

main()
