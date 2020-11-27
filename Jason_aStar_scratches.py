# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 10:06:26 2020

@author: jason
"""

import collections 
import heapq

f = open("...\\sokoban00.txt", 'r')
sizeH = ""
sizeV = ""
storLoc = ""
wallSquares = ""
board = ""
mp = ""


def parse(txt):
    """
    parser for the input file, reads off the game specification
    and initializes the game board as a 2D-array
    """
    global sizeH, sizeV, storLoc, wallSquares, board, mp
    def group(line):
        """
        given a line in the input file, return a list [num, [x1,y1][x2,y2],...,[xn,yn]]
        where num is the number of objects (walls, boxes, etc) and 
        the [x,y] tuples are coordinates.
        """
        toCount = len(line)
        if toCount % 2 == 0:
            re = [line[i:i+2] for i in range(0,len(line),2)]
            return re
        elif toCount % 2 == 1:
            re = [line[0]]+[line[i:i+2] for i in range(1,len(line),2)]
            return re
        
    # read file, break file into separate lines
    specstring = [l.strip() for l in txt]
    
    # turning specstring to integers
    spec = []
    for i in range(len(specstring)):
        spec = spec + [list(map(int, specstring[i].split()))]

    
    # initial configuration of the board, to be read off from spec
    # the game board is implemented as a 2D matrix
    # freespace = "0" wall = "1", box = "2", storage = "3", player = "4", on-goal = "5"
    
    sizeH, sizeV = spec[0]
    board = [["0" for x in range(sizeH)] for y in range(sizeV)]
    
    wallSpec = group(spec[1])
    boxSpec = group(spec[2])
    storSpec = group(spec[3])
    
    # saving the coordinates; doing the "minus one" because arrays start counting at zero
    boxLoc = tuple(map(lambda x: tuple([x[0]-1, x[1]-1]), boxSpec[1:]))
    storLoc = tuple(map(lambda x: tuple([x[0]-1, x[1]-1]), storSpec[1:]))
    wallSquares = tuple(map(lambda x: tuple([x[0]-1, x[1]-1]), wallSpec[1:]))
    
    # first check if some boxes are on goal
    
    onGoal = [i for i in boxLoc if i in storLoc]

    player = spec[4]
    x,y = player
    board[x-1][y-1] = "4"

    for i in range(len(wallSquares)):
        x, y = wallSquares[i]
        board[x][y] = "1"
    
    for i in range(len(storLoc)):
        x, y = storLoc[i]
        board[x][y] = "3"
        
    for i in range(len(boxLoc)):
        x, y = boxLoc[i]
        board[x][y] = "2"
    
    if onGoal:
        for i in range(len(onGoal)):
            x, y = onGoal[i]
            board[x][y] = "5"
    
    # finally, print the game map as a text, saving the text string
    # to the variable mp (for "map")
    

    # showBoard(board)
    

def showBoard(board):
    """prints the game as a string"""
    global sizeV, mp    
    for i in range(sizeV):
        if not mp:
            mp += (''.join(board[i]))
        else: 
            mp += "\n"+(''.join(board[i]))
    print(mp)


def getPlayer(board):
    for i in range(sizeV):
        if "4" in board[i]:
            return (i, board[i].index("4"))
    
def getBoxes(board):
    boxes = []
    for i in range(sizeV):
        if "2" in board[i]:
            boxes.append([i, board[i].index("2")])
    return tuple(map(tuple,boxes))

def goalCheck(boxes):
    """check if the game is in goal state"""
    return sorted(boxes) == sorted(storLoc)


def isLegalMove(board, action):
    """Check if a move is allowed"""
    x, y = getPlayer(board)
    boxes = getBoxes(board)
    if action[-1].isupper(): # check if move is a push, if so, look at two spaces away from intended action
        x1, y1 = x + 2 * action[0], y + 2 * action[1]
    else: 
        x1, y1 = x + action[0], y + action[1]
    return (x1, y1) not in boxes + wallSquares #false if you're pushing a box/running into in box or wall


# actions have the form [-1,0,'u','U']


def updateBoard(player, boxes, action): # want to run a isLegalMove check before calling this function
    global board    
    x, y = player # get the current coordinates of the player
    newPlayer = [x+action[0], y+action[1]] #update player coordinates resulting from an action

    if action[-1].isupper(): # check if action is a push
        boxes = [list(x) for x in boxes] #turn boxes into a list, so we can modify it
        boxes.remove(newPlayer)
        boxes.append([x + 2 * action[0], y + 2 * action[1]])
        boxes = tuple(tuple(x) for x in boxes)
    newPlayer = tuple(newPlayer)
    
    return newPlayer, boxes





def possibleMoves(player, boxes):
    """input a board, return all possible legal moves"""
    directions = [[-1,0,'u','U'],[1,0,'d','D'],[0,-1,'l','L'],[0,1,'r','R']]
    x0, y0 = getPlayer(board)
    legalMoves = []
    for action in directions:
        x1, y1 = x0 + action[0], x0 + action[1]
        if (x1, y1) in boxes: # we hit a box
            action.pop(2) # remove the lower case letter
        else:
            action.pop(3) # remove the upper case letter
        if isLegalMove(board, action):
            legalMoves.append(action)
        else: 
            continue     
    return tuple(tuple(x) for x in legalMoves) 

def BFS(board):
    """bredth-first search"""
    boxes = getBoxes(board)
    player = getPlayer(board)

    starting = (player, boxes) # a tuple, left-hand-side is player position, right-hand-side is box coordinates
    frontier = collections.deque([[starting]]) # creates a search frontier
    actions = collections.deque([[0]]) 
    visited = set()
    while frontier:
        node = frontier.popleft()
        node_action = actions.popleft() 
        if goalCheck(node[-1][-1]):
            print(','.join(node_action[1:]).replace(',',''))
            break
        if node[-1] not in visited:
            visited.add(node[-1])
            for action in possibleMoves(node[-1][0], node[-1][1]):
                newPlayer, newBoxes = updateBoard(node[-1][0], node[-1][1], action)
                # if deadEndCheck(newBoxes):
                # have to think about what to check for dead ends
                #     continue
                frontier.append(node + [(newPlayer, newBoxes)])
                actions.append(node_action + [action[-1]])


parse(f)

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

def aStarSearch():
    """Implement A* search, modifying from BFS, but with PriorityQueue as data structure for search space"""
    # these are the same as in BFS
    boxes = getBoxes(board)
    player = getPlayer(board)
    starting = (player, boxes)
    visited = set()

    # implementing frontier and actions as priority queues. Priority is determined by heuristic function
    frontier = PriorityQueue()
    # frontier.push([starting], heuristic(player, boxes))
    # heuristic(player, boxes) to be filled in by Hamza.
    actions = PriorityQueue()
    # actions.push([0], heuristic(player, starting[1]))
    # also waiting for heuristic(player, starting[1])
    
    while frontier:
        node = frontier.pop()
        node_action = actions.pop()
        if goalCheck(node[-1][-1]):
            print(','.join(node_action[1:]).replace(',',''))
            break
        if node[-1] not in visited:
            visited.add(node[-1])
            # Cost = cost(node_action[1:]) #need to define a cost function. Simplest way is to have
            # every non-push step have cost 1. Something like
            # def cost(actions): return len([x for x in actions if x.islower()])
            for action in possibleMoves(node[-1][0], node[-1][1]):
                newPlayer, newBoxes = updateBoard(node[-1][0], node[-1][1], action)
                # if deadEndCheck(newBoxes):
                # have to think about what to check for dead ends
                #     continue
                
                # Heuristic = heuristic(newPlayer, newBoxes) waiting for the heuristic function
                frontier.push(node + [(newPlayer, newBox)], Heuristic + Cost) 
                actions.push(node_action + [action[-1]], Heuristic + Cost)


