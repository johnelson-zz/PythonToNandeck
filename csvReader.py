
class csvReader(object):

	def __init__(self, filename):
		self.filename = filename
		self.columns = None
		self.dataByCol = {}
		self.dataByRow = []
		self.read()

	def read(self):
		self.read = True
		self.columns = None
		self.dataByCol = {}
		self.dataByRow = []
		with open(self.filename, "r") as rFile:
			lineNum = 0
			for line in rFile:
				splitLine = [s.strip() for s in line.split(",")]
				building = []
				for sl in splitLine:
					if len(sl) <= 1:
						newString = sl
					elif sl[0] == "'" and sl[-1] == "'":
						newString = sl[1:-1]
					elif sl[0] == "\"" and sl[-1] == "\"":
						newString = sl[1:-1]
					else:
						newString = sl
					building.append(newString.strip())
				splitLine = building
				if self.columns is None:
					self.columns = splitLine
				else:
					buildingDataByRow = {x : None for x in self.columns}
					for index in range(len(splitLine)):
						try:
							buildingDataByRow[self.columns[index]] = splitLine[index]
							self.dataByCol[self.columns[index]].append(splitLine[index])
						except IndexError:
							print str(lineNum) + " - Ignoring extra data: " + str(splitLine[index])
							break
						except KeyError:
							self.dataByCol[self.columns[index]] = []
					self.dataByRow.append(buildingDataByRow)
				lineNum += 1

	def getColumnsNames(self):
		return self.columns

	def getColumn(self, col):
		return self.dataByCol[col]

	def getRow(self, index):
		return self.dataByRow[index]

	def __iter__(self):
		return iter(self.dataByRow)
			
			


