import sys, inspect, collections

class nObject(object):
	"""
	An nObject is a nandeck object. Most of these correspond to nandeck commands, but some (like cards and cRanges) don't directly correspond to any particular line in the final nandeck file.
	You shouldn't need to define your own nObjects unless you're implementing nandeck commands that aren't currently implemented.
	"""

	mandatoryAttr = []	#list of attributes that have to be defined for the nObject to make sense
	stringAttr = []		#list of attributes that should be surrounded by "" in the final file
	colorAttr = []		#list of attributes that are html colors
	flags = []		#list of attributes that are flags (and can be set singly, or in combination)
	nandeckEnums = []	#list of enums for this function that nandeck will recognize (ie, left, center)
	addsOn = False 		#instead of having more than one of this object per card, they combine (text mostly)
	maxRound = 0		#how many rounds of validation (after the first) this object takes.
	             		#if this object depends on another type of object being valid, it needs to
	              		#last at least 1 round longer than that object
	isCard = False		#this isn't a card. 

	nandeckString = "I initialized an nObject directly. Oops." #This object's nandeck name. ie, RECTANGLE or TEXT
	nObjectType = "nObject"	#The name of the id group with which you want to keep track of this class of objects
	
	hasRange = True 	#whether or not the object has a range that needs to be calculated

	# these are probably universal
	notSettingParams = ["self", "preset"]
	notNanDeckParams = ["self", "preset", "deck", "font"]
	notEqualityParams= ["self", "preset", "cRange"]

	def customInit(self):
		"""
		Called after the normal nObject init
		"""
		pass


	def customValidation(self, deck):
		"""
		define your own validation function.
		return None if there's no error, or a string with an error message
		"""
		return None

	def info(self):
		"""
		a quicker, hopefully more useful version of str()
		"""
		return "nObject example"
		pass

	def preValidateAdjust(self):
		"""
		called before calling validate.
		useful for conditional nandeck parameters. For example, Rectangle has 2 color parameters
		if both are defined, they're inner and then outer
		if only one is defined, it's outer.
		"""
		pass

	def examplePreset(self):
		"""
		if you put preset="example" in an in object, it will call this function after the normal initialization
		"""
		pass

	@staticmethod
	def x_waitsForDirectly_y(x, y):
		try:
			getattr(x, "__iter__")
		except AttributeError:
			x = [x]
		try:
			getattr(y, "__iter__")
		except AttributeError:
			y = [y]
			
		for X in x:
			for Y in y:
				X.waitForDirectly.append(Y)
				Y.awaitedDirectly.append(X)

	@staticmethod
	def x_waitsFor_y(x, y):
		try:
			getattr(x, "__iter__")
		except AttributeError:
			x = [x]
		try:
			getattr(y, "__iter__")
		except AttributeError:
			y = [y]
			
		for X in x:
			for Y in y:
				X.waitFor.append(Y)
				Y.awaited.append(X)


	def __init__(self, parameters):
		self.output = None
		self.parameters = parameters
		self.nanDeckParams= [] # things that will be printed in the nandeck output string

		# it's often important to notice if 2 nandeck commands are functionally identical
		# (for the purposes of ranges, etc). If a parameter isn't relevant to that, 
		# then add it to notEqualityParams
		self.equalitySet = set()

		# if object X has __init__(self, a, b, c) this assigns 
		# X.a = <whatever a was>, X.b = <whatever b was>, etc
		# Any args in notSettingParams won't be set this way.
		argList = inspect.getargspec(self.__class__.__init__)
		for arg in argList.args:
			if not arg in self.notSettingParams:
				setattr(self, arg, self.parameters[arg]) 
			if not arg in self.notNanDeckParams:
				self.nanDeckParams.append(arg)
			if not arg in self.notEqualityParams:
				self.equalitySet.add(arg)

		self.waitFor = []
		self.waitForDirectly = []
		self.awaited = []
		self.awaitedDirectly = []

		self.customInit()
		try:
			#this lets you define multiple default values for an nObject 
			preset = self.parameters["preset"]
		except KeyError:
			#function has no presets
			preset=None
			pass

		if preset is not None:
			presetName = str(preset)+"Preset"
			try:
				presetFunc = getattr(self, presetName)
			except AttributeError:
				print "Tried to call missing preset function " + str(presetName)
			else:
				presetFunc()
		try:
			self.deck.getID(self)
		except AttributeError:
			print "Error: nObject doesn't have a deck!"
			raise

		#print "initialized " + str(self.__class__) + " with info " + self.info()

	def equivalent(self, other):
		"""
		determines if 2 nObjects are functionally identical
		"""
		if self.nObjectType != other.nObjectType:
			return False
		combinedSet = self.equalitySet.union(other.equalitySet)
		for arg in combinedSet:
			try:
				if getattr(self, arg) != getattr(other, arg):
					return False
			except AttributeError:
				return False
		return True

	def addToNObject(self, nFeature):
		"""
		If this type of nObject merges instead of haivng multiples, use this function to do it.
		for example, if a card has only 1 spot for rules text, but multiple rules text nObjects, those
		nObjects should merge into one object.
		"""
		pass

	def outputString(self, rangeString):
		"""
		if this nObject translates to a line in an nandeck file, this function builds that line
		"""
		buildingString = self.nandeckString + " = "
		for key in self.nanDeckParams:
			if key == "cRange":
				buildingString += "%(cRange)s, "
			else:
				value = getattr(self, key)
				buildingString += nObject.param(value) 
		self.output = nObject.cleanup(buildingString) % {"cRange" : rangeString}
		return self.output

	@staticmethod
	def param(string):
		"""
		helper function for building the output string
		"""
		return str(string)+", " if string is not None else ""

	@staticmethod
	def cleanup(string):
		"""
		helper function for building the output string
		"""
		while string[-2:] == ", ":
			string = string[:-2]
		return string

	def validate(self, deck):
		"""
		Sanity checks the object
		has all of its mandatory attributes
		colors are html colors, strings are enclosed in quotes, etc
		"""
		self.preValidateAdjust()
		missing = []
		errorMessage = None
		for key in self.nanDeckParams:
			missing = False
			try:
				value = getattr(self, key)
			except AttributeError:
				value = None
			if value is None:
				missing = True
			if key in self.mandatoryAttr and missing:
					return "Missing mandatory attribute " + str(key)
			elif missing:
				continue
			elif key in self.stringAttr:
				if value is None or len(value) == 0:
					value = ""
				else:
					value = str(value)
					if value[-1] != "\"":
						value += "\""
					if value[0] != "\"":
						value = "\"" + value
				setattr(self, key, value)
			elif key in self.colorAttr and value is not None:
				value = value.trim()
				errorMessage = None
				def lenCheck(value):
					if len(value) == len("#000000"):
						return None
					else:
						return "Invalid Length"
				def firstCharacter(value):
					if value[0] == '#':
						return None
					else:
						return "Invalid first character"
				def charRanges(value):
					if reduce( lambda x, y: x and y, [ x in "0123456789ABCDEF" for x in value[1:] ] ):
						return None
					else:
						return "Invalid characters"
				if value != "EMPTY":
					validityChecks = [lenCheck, firstCharacter, charRanges]
					for check in validityChecks:
						result = check(value)
						errorMessage = result if errorMessage is None else errorMessage+"\n"+result
					if errorMessage is not None:
						return errorMessage
			else:
				if value in self.nandeckEnums:
					return None
				if type(value) == type(1) or type(value) == type(1.0):
					return None
				allFlags = True
				for c in value:
					if c not in self.flags:
						allFlags = False
						break
				if allFlags:
					return None
				return "Error: unrecognized variable format for value " + str(value)
		return self.customValidation(deck)

