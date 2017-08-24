import sys, inspect, collections
from nObject import nObject

showWarnings = False

class deck(object):

	hiLow = collections.namedtuple("hiLow", ['low', 'high'])
	outputOrder = ["cardsize", "rect", "text"]
	outputOrderLast = []
	roundOrder = []
	roundOrderLast = []

	def getID(self, idee):
		if idee.isCard:
			self.cards.append(idee)
			idee.id = len(self.cards)
		elif idee.nObjectType == "nObject":
			print "Error: nObject is being directly initialized!"
			idee.id = None
		else:
			try:
				self.nObjectTypeDict[idee.nObjectType].append(idee)
			except KeyError:
				self.nObjectTypeDict[idee.nObjectType] = [idee]
			idee.id = len(self.nObjectTypeDict[idee.nObjectType])

	def __init__(self, name):
		self.name = name
		self.nObjectTypeDict = {}
		self.cards = []
		self.rawLines = []
		self.orderedLines = []
		self.customInit()

	def customInit(self):
		pass

	@staticmethod
	def interpValidation(pString):
		if pString is not None:
			print pString
			return False
		return True

	@staticmethod
	def buildExecutionList(first, last, generalDict):
		executionList = []
		for f in first:
			try:
				executionList.append(generalDict[f])
			except KeyError:
				pass
		for leftovers in generalDict.iterkeys():
			if leftovers not in first and leftovers not in last:
				executionList.append(generalDict[leftovers])
		for l in last:
			if l not in first:
				try:
					executionList.append(generalDict[l])
				except KeyError:
					pass
		return executionList
	
	def makeTheDeck(self):
		success = True
		maxRound = 0
		round = 0
		while round <= maxRound:
			executionList = deck.buildExecutionList(self.roundOrder, self.roundOrderLast, self.nObjectTypeDict)
			for nObjectList in executionList:
				for no in nObjectList:
					skip = False
					if round == 0:
						try:
							nextRoundFunc = getattr(no, "validate")
						except AttributeError:
							continue
						maxRound = maxRound if maxRound > no.maxRound else no.maxRound
					else:
						try:
							nextRoundFunc = getattr(no, "round"+str(round)+"Validation")
						except AttributeError:
							continue
					success = deck.interpValidation(nextRoundFunc(self))
					if not success:
						break
				if not success:
					break	
			round += 1
		if success:
			self.createRanges()
			self.createOutputLines()
			if deck.arrangeLines(self.rawLines, self.orderedLines):
				self.writeToFile("output/" + str(self.name)+".txt")
			else:
				print "Failed to arrange all of the lines."
				print "\nThe following nObjects were placed: " 
				for x in self.orderedLines:
					print str(x.nObjectType) + " " + str(x) + ":  " + str(x.output)
				print "\n\nThe following nObjects could not be placed:  "
				for x in self.rawLines:
					print str(x.nObjectType) + " " + str(x) + ":  " + str(x.output)
					print "waiting for:"
					for w in x.waitFor:
						print "  " + str(w.nObjectType) + " " + str(w) + ":  " + str(w.output)
					print "waiting for directly:"
					for w in x.waitForDirectly:
						print "  " + str(w.nObjectType) + " " + str(w) + ":  " + str(w.output)

	def createRanges(self):
		alreadyRanged = [] 
		for nObjectTypeList in self.nObjectTypeDict.itervalues():
			for no in nObjectTypeList:

				#objects with ranges only
				if not no.hasRange:
					continue

				#make sure we didn't get this one already
				dupe = False
				for ar in alreadyRanged:
					if ar.equivalent(no):
						dupe = True
						break
				if dupe:
					no.id = None
					continue

				#look for all similar features to create a range
				hitOnce = False
				completedSet = False
				idList = []
				firstIn = -1
				lastIn =  -1 
				result = []
				for x in range(len(self.cards)):
					if self.cards[x].hasNObject(no):
						if firstIn == -1:
							firstIn = x
							lastIn = x
						else:
							lastIn = x
						if x == len(self.cards)-1:
							completedSet = True
					elif firstIn != -1:
							completedSet = True
					if completedSet:
						if firstIn != lastIn:
							result.append(str(1+firstIn)+"-"+str(1+lastIn))
						else:
							result.append(str(1+firstIn))
						firstIn = -1
						lastIn = -1
						hitOnce = True
						completedSet = False
				no.cRange = result
				alreadyRanged.append(no)
				if not hitOnce:
					if showWarnings:
						print "Warning: " +str(no) + ", " + str(no.info()) + " isn't used at all."

	def createOutputLines(self):
		for nObjectList in self.nObjectTypeDict.itervalues():
			for no in nObjectList:
				if no.id is None:
					no.output = None
					#continue
				elif no.hasRange and (no.cRange is None or len(no.cRange) == 0):
					no.output = None
					#continue
				else:
					rangeString = ""
					if no.hasRange:
						if len(no.cRange) > 1: 
							rangeString =  "\""
							rangeString += ",".join(no.cRange)
							rangeString += "\""
						else:
							rangeString = "\"" + no.cRange[0] + "\""
					no.outputString(rangeString)
				self.rawLines.append(no)

	@staticmethod
	def arrangeLines(lList, orderedList):
		"""
		Builds the dict to help out workingArrangeLines
		wrapper function for recursion
		"""
		outputTypeDict = {}
		for l in lList:
			try:
				outputTypeDict[l.nObjectType].append(l)
			except KeyError:
				outputTypeDict[l.nObjectType] = [l]

		return deck.workingArrangeLines(outputTypeDict, lList, orderedList)

	@staticmethod
	def workingArrangeLines(outputTypeDict, lList, orderedList): 
		"""
		recursive
		returns False if something went wrong
		returns True and adds to orderedList otherwise
		"""
		if len(lList) == 0:
			print "Attempting to arrange an empty list"
			return False
		startingPoint = None
		for index in range(len(lList)):
			if len(lList[index].waitFor) == 0 and len(lList[index].waitForDirectly) == 0:
				startingPoint = lList[index]
				break
		if startingPoint is None:
			# if there's no node that doesn't have requirements, we're done
			return False 

		#ok, we're adding this node to the list
		orderedList.append(startingPoint)
		lList = lList[:index] + lList[index+1:]

		#if we're done, let's just be done
		if len(lList) == 0:
			return True
	
		#remove it from the dict of outstanding nodes:
		outputTypeDict[startingPoint.nObjectType] = [x for x in outputTypeDict[startingPoint.nObjectType] if not x.equivalent(startingPoint)]

		# next, remove this from all "waits"
		
		for x in startingPoint.awaited:
			x.waitFor = [ y for y in x.waitFor if not y.equivalent(startingPoint) ]

		#next, find everyone with this as a waitForDirectly
		# remove this from their directly beforeMe list
		for x in startingPoint.awaitedDirectly:
			x.waitForDirectly = [ y for y in x.waitForDirectly if not y.equivalent(startingPoint) ]

		# now, every node of the same type as this node needs 
		# to wait for everyone who was waiting on this node
		nObject.x_waitsFor_y(x=outputTypeDict[startingPoint.nObjectType], y=startingPoint.awaitedDirectly)

		#finally, append to orderedList and remove from lList
		return deck.workingArrangeLines(outputTypeDict, lList, orderedList) 
				

	def writeToFile(self, destination):
		with open(destination, 'w') as dFile:
			for ol in self.orderedLines:
				if ol.output is None:
					continue
				dFile.write(ol.output)
				dFile.write("\n")
			
