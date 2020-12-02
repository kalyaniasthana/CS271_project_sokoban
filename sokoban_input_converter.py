import os

class SokobanInputConverter:

    def __init__(self, boardInputFile, number):
        # initialise board variables
        self.sizeH, self.sizeV, self.nWallSquares, self.wallCoordinates, self.nBoxes, \
        self.boxCoordinates, self.nstorLocations, self.storCoordinates, self.playerLoc = \
        0, 0, 0, [], 0, [], 0, [], ()
        self.boardInputFile = boardInputFile
        self.number = number

    def parse(self): # parse input file - inputXY.txt to sokobanXY.txt

        """Explanation ...."""
        assert os.path.isfile(self.boardInputFile)
        with open(self.boardInputFile) as fin:
            countLines = 0
            for line in fin:
                currentLine = list(line.strip('\n'))
                if countLines == 0:
                    self.sizeH = len(currentLine)
                for c in range(self.sizeH):
                    currentChar = currentLine[c]
                    self.adder(currentChar, c, countLines)
                countLines += 1
        self.sizeV = countLines
        self.writing_on_file()

    def adder(self, char, i, j): # converts a square in inputXY depending on its content
        if char == '@':
            self.playerLoc = (j+1, i+1)
        elif char == '#':
            self.nWallSquares += 1
            self.wallCoordinates.append((j+1, i+1))
        elif char == '$':
            self.nBoxes += 1
            self.boxCoordinates.append((j+1, i+1))
        elif char == '.':
            self.nstorLocations += 1
            self.storCoordinates.append((j+1, i+1))

    def writing_on_file(self):
        path = os.path.join(os.getcwd(), "input_files", "sokoban"+self.number+".txt")
        with open(path, "w") as fout:
            # Line 1 is the sizeH, sizeV
            fout.write(str(self.sizeH)+" "+str(self.sizeV)+"\n")
            # Line 2 is the number of walls and the list of wall coordinates
            fout.write(str(self.nWallSquares))
            for wallCoord in self.wallCoordinates:
                fout.write(" "+str(wallCoord[0])+" "+str(wallCoord[1]))
            fout.write("\n") # linebreak
            # Line 3 is the number of boxes and the list of box coordinates
            fout.write(str(self.nBoxes))
            for boxCoord in self.boxCoordinates:
                fout.write(" "+str(boxCoord[0])+" "+str(boxCoord[1]))
            fout.write("\n") # linebreak
            # Line 4 is the number of storage places and the list of storage coordinates
            fout.write(str(self.nstorLocations))
            for storCoord in self.storCoordinates:
                fout.write(" "+str(storCoord[0])+" "+str(storCoord[1]))
            fout.write("\n") # linebreak
            # Line 5 is the initial position of player
            fout.write(str(self.playerLoc[0])+" "+str(self.playerLoc[1]))

def main():
    print("Enter XY for the inputXY.txt you want to convert to sokobanXY.txt (example 01)")
    strFileNumber = str(input())
    boardInputFile = os.path.join(os.getcwd(), 'input_files', 'input'+strFileNumber+'.txt')
    sokobanBoard = SokobanInputConverter(boardInputFile, strFileNumber)
    sokobanBoard.parse()

main()
