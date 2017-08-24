from nanDeck import *

class nImage(nObject):

	mandatoryAttr = ["imageFile", "x", "y", "width", "height", "angle"]
	stringAttr = ["imageFile"]
	colorAttr = []
	flags = ["flag"]
	nandeckEnums = ["P", "A", "G", "H", "V", "T", "X", "N", "R", "D", "C"]

	nandeckString = "IMAGE"
	nObjectType = "image"

	def __init__(self, deck, cRange=None, imageFile=None, x=None, y=None, width=None, height=None, angle=0, imageFlags=None, alphaChannel=None, textureWidth=None, textureHeight=None, skewHorz=None, skewVert=None, preset=None):
		nObject.__init__(self, locals())

	def customValidation(self, deck):
		"""
		define your own validation function.
		return None if there's no error, or a string with an error message
		"""
		try:
			with Open(self.imageFile, "r") as temp:
				pass
		except:
			print "Error: couldn't open imageFile for " + str(self.info())
			raise
		return None

	def info(self):
		"""
		a quicker, hopefully more useful version of str()
		"""
		return "Image file: " + str(self.imageFile)

	def behind(self, bList):
		deck.x_waitFor_y(x=bList, y=self)

