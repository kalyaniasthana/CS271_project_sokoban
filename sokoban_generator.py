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
