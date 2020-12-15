import os
from board import Board
from game import Game

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
	#print(game.play_AStar())
	print(game.play_AStar_fix_f())
	#print(game.play_IDAStar())
	print('Tree Depth: {}, Average Branching Factor: {}'.format(game.treeDepth, game.branchingFactor))
	# moves = list('rDlddrrruuLLrrddllUdrruulullDRddl')
	# print(len(moves))
	# game.play_moves(moves)

if __name__ == '__main__':
	main()
