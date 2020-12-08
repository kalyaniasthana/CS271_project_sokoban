class Heuristic:
	def __init__(self):
		self.name = None

	def set_heuristic(self, name):
		self.name = name

	def calculate(self, storCoordinates, boxCoordinates):
		heuristicVal = 0
		if self.name == "manhattan" or self.name == None:
			for box in boxCoordinates:
				for storage in storCoordinates:
					heuristicVal += (abs(storage[0] - box[0])+abs(storage[1] - box[1])) # WHAT THE HECK DO storage() AND box() RETURN? 
		elif self.name == "euclidean":
			for box in boxCoordinates:
				for storage in storCoordinates:
					heuristicVal += sqrt((abs(storage[0] - box[0])^2+abs(storage[1] - box[1])^2))

		return heuristicVal