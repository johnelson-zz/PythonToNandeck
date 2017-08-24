import sys, inspect, collections


class featureList(object):
	def __init__(self, pList=None):
		if pList is None:
			self.mList = []
		elif type(pList) == list:
			self.mList = pList[:]
		elif type(pList) == featureList:
			self.mList = pList[:]
		else:
			self.mList = [pList]
		#print "initialized feature list with features: " + str(self.mList)

	def __iter__(self):
		return iter(self.mList)


	def __getitem__(self, x=None):
		if x is None:
			return self.mList[:]
		else:
			return self.mList[x]	

	def append(self, newValue):
		self.mList.append(newValue)

class card(object):

	border = 0.5
	width = 6
	height = 9
	workingHeight = height - (2*border)
	workingWidth = width - (2*border)
	isCard = True

	@staticmethod
	def generateCards(number, deck, tags=None, features=None):
		result = []
		for x in range(number):
			result.append(card(deck, tags, featureList(features)))
		return result
			
        def __init__(self, deck, tags=None, features=None):
		"""
		This is a card.
		"""
		self.nandeckString = "card"
		self.deck = deck
		self.deck.getID(self)
		if tags is None:
			self.tags = []
		elif type(tags) == type([1, 2]):
			self.tags = tags 
		else:
			self.tags = [tags]
		self.features = featureList(features)
		if features is not None:
			for f in self.features:
				if f.deck != self.deck:
					print "Error: deck mismatch between card and addon!"
					raise TypeError

	def addFeature(self, nFeature):
		if nFeature.addsOn:
			for f in self.features:
				if f.nObjectCardType == nFeature.nObjectCardType:
					f.addToNObject(nFeature)
					f.id = None
					return
		self.features.append(nFeature)

	def customValidate(self):
		return None

	def validate(self):
		for a in self.features:
			try:
				if a.deck != self.deck:
					return "Error: " + str(a) + " isn't in the same deck as card " + str(self) + " id " + str(self.id)
			except AttributeError:
				return "Error: '" + str(a) + "' isn't a feature at all, or is a feature with no deck."
		return None

	@staticmethod
	def createRanges(featureList, cards):
		alreadyRanged = [] 
		for feature in featureList:
			if not feature.hasRange:
				continue
			dupe = False
			for ar in alreadyRanged:
				if ar.equivalent(feature):
					dupe = True
					break
			if dupe:
				#feature.cRange = None
				feature.id = None
				continue
					
			hitOnce = False
			completedSet = False
			idList = []
			firstIn = -1
			lastIn =  -1 
			result = []
			for x in range(len(cards)):
				InFeatureList = False
				for cf in cards[x].features:
					if feature.equivalent(cf):
						InFeatureList = True
						break	
				if InFeatureList:
					if firstIn == -1:
						firstIn = x
						lastIn = x
					else:
						lastIn = x
					if x == len(cards)-1:
						completedSet = True
				elif firstIn != -1:
						completedSet = True
				if completedSet:
					result.append(str(1+firstIn)+"-"+str(1+lastIn))
					firstIn = -1
					lastIn = -1
					hitOnce = True
					completedSet = False
				
			feature.cRange = result
			alreadyRanged.append(feature)
			if not hitOnce:
				print "Warning: " +str(feature) + ", " + str(feature.info()) + " isn't used at all."

				
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
			for nObjectList in self.nObjectTypeDict.itervalues():
				card.createRanges(nObjectList, self.cards)
			self.createOutputLines()
			if deck.arrangeLines(self.rawLines, self.orderedLines):
				self.writeToFile(str(self.name)+".txt")
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

		#for line in lList:
			#for requirementList in [l.waitFor, l.waitForDirectly, l.awaited, l.awaitedDirectly]:
				#index = 0
				#while index < len(requirementList):
					#if requirementList[index] in outputTypeDict[requirementList[index].nObjectType]:
						#index += 1
					#else:
						#requirementList.pop(index)
		#for key, value in outputTypeDict.iteritems():
			#print "key: " + str(key)
			#for v in value:
				#print "  " + str(v) + ":  " + str(v.output)
		return deck.workingArrangeLines(outputTypeDict, lList, orderedList)

	@staticmethod
	def workingArrangeLines(outputTypeDict, lList, orderedList): 
		"""
		recursive
		returns False if something went wrong
		returns True and adds to orderedList otherwise
		"""
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
		with open(destination, 'a') as dFile:
			for ol in self.orderedLines:
				if ol.output is None:
					continue
				dFile.write(ol.output)
				dFile.write("\n")
			
