import sys, inspect, collections
from nObject import nObject

class featureList(object):
	"""
	Helper class for card. basically an improved list
	"""
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
		if newValue.addsOn:
			for oldValue in self.mList:
				if oldValue.nObjectType == newValue.nObjectType:
					newValue.addToNObject(oldValue)
					newValue.id = None
					return
		self.mList.append(newValue)

class card(object):
	"""
	A container for multiple features (nObjects) that is aware of some of the properties of nObjects
	card knows that sometimes nObjects add onto each other
	cards know that they go into decks
	"""

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

		self.customInit()

	def customInit(self):
		pass

	def hasNObject(self, lookingFor):
		for f in self.features:
			try:
				if f.equivalent(lookingFor):
					return True
			except AttributeError:
				break
		return False

	def customValidate(self):
		return None

	def info(self):
		return "Card with tags: " + str(self.tags) 

	def validate(self):
		for a in self.features:
			try:
				if a.deck != self.deck:
					return "Error: " + str(a) + " isn't in the same deck as card " + str(self) + " id " + str(self.id)
			except AttributeError:
				return "Error: '" + str(a) + "' isn't a feature at all, or is a feature with no deck."
		return None

