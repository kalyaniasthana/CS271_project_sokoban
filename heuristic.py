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
					heuristicVal += (abs(storage[0] - box[0])+abs(storage[1] - box[1]))
		elif self.name == "euclidean":
			for box in boxCoordinates:
				for storage in storCoordinates:
					heuristicVal += sqrt((abs(storage[0] - box[0])^2+abs(storage[1] - box[1])^2))
		elif self.name == "manhattan2" or self.name == None:
			for box in boxCoordinates:
				smallestBoxDist = 1000
				for storage in storCoordinates:
					dist_box_to_storage = (abs(storage[0] - box[0])+abs(storage[1] - box[1]))
					if dist_box_to_storage < smallestBoxDist:
						smallestBoxDist =  dist_box_to_storage
				heuristicVal += smallestBoxDist
		elif self.name == "euclidean2":
			for box in boxCoordinates:
				smallestBoxDist = 1000
				for storage in storCoordinates:
					dist_box_to_storage = sqrt((abs(storage[0] - box[0])^2+abs(storage[1] - box[1])^2))
					if dist_box_to_storage < smallestBoxDist:
						smallestBoxDist =  dist_box_to_storage
				heuristicVal += smallestBoxDist

		return heuristicVal
