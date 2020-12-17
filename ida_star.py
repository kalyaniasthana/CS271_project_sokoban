def play_IDAStar(self):
    start = time()
    rootNode = deepcopy(self.board)

    if not rootNode.get_stor_coordinates():
        end = time()
        return 'THERE ARE NO STORAGE LOCATIONS!', (end - start)
    if not rootNode.get_box_coordinates():
        end = time()
        return 'THERE ARE NO BOX LOCATIONS!', (end - start)
    if not rootNode.get_player_loc():
        end = time()
        return 'SOKOBAN PLAYER MISSING!', (end - start)
    if rootNode.is_goal_state():
        end = time()
        return 'BOARD IS ALREADY IN GOAL STATE!', (end - start)

    H = Heuristic()
    heuristicVal = H.calculate(rootNode.get_stor_coordinates(), rootNode.get_box_coordinates())

    bound = heuristicVal
    frontier1 = PriorityQueue()
    frontier2 = PriorityQueue()
    path = PriorityQueue()

    frontier1.push(rootNode, heuristicVal)
    frontier2.push((rootNode.get_player_loc(), rootNode.get_box_coordinates()), heuristicVal)
    path.push([''], heuristicVal)
    visited = []

    while(True):
        print('Frontier 1 Length: {}, Bound Value: {}'.format(
            len(frontier1.Heap), bound))
        f_value = self.bounded_AStar(path, 0, bound, frontier1, frontier2, visited, H)
        if f_value == FOUND:
            end = time()
            return moves, bound
        if f_value > 100000:
            return NOT_FOUND
        bound = f_value
    return True

def bounded_AStar(self, path, g, bound, frontier1, frontier2, visited, H):
    currentNode = frontier1.get_last()
    (currentPlayer, currentBoxCoordinates) = frontier2.get_last()
    currentMove = path.get_last()
    f = g + H.calculate(currentNode.get_stor_coordinates(), currentNode.get_box_coordinates())
    min_value = 10000
    if f > bound:
        return f
    if currentNode.is_goal_state():
        return FOUND

    possibleMoves = currentNode.possible_moves()
    visited.append((currentPlayer, currentBoxCoordinates))

    for move in possibleMoves:
        childNode = deepcopy(currentNode)
        childNode.update_board(move)
        if (childNode.get_player_loc(), childNode.get_box_coordinates()) not in visited:
            if self.is_deadlock(childNode):
                print('DEADLOCK CONDITION')
                continue
            heuristicVal = H.calculate(childNode.get_stor_coordinates(), childNode.get_box_coordinates())
            frontier1.push(childNode, heuristicVal + g + 1)
            frontier2.push((childNode.get_player_loc(), childNode.get_box_coordinates()), heuristicVal + g + 1)
            path.push(currentMove + [move], heuristicVal)
            f_value = self.bounded_AStar(path, g + 1, bound, frontier1, frontier2, visited, H)
            if f_value == FOUND:
                return FOUND
            if f_value < min_value:
                min_value = f_value
            currentNode = frontier1.pop()
            (currentPlayer, currentBoxCoordinates) = frontier2.pop()
            currentMove = path.pop()
    return min_value
