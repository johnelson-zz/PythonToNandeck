from nObject import nObject

class nFont(nObject):
	hasRange = False
	mandatoryAttr = ["fontName", "size", "charColor"]
	stringAttr = ["fontName"]
	colorAttr = ["charColor", "backgroundColor"]
	flags = ["B", "I", "U", "S", "T", "N", "C", "R", "H", "Q", "E", "Z", "F", "V", "P", "O", "D", "G"]
	nandeckEnums = []
	nandeckString = "FONT"
	nObjectType = "font"

	def __init__(self, deck, fontName=None, size=None, style=None, charColor=None, backgroundColor=None, outlineX=None, outlineY=None, stepX=None, stepY=None, preset=None):
		nObject.__init__(self, locals())

	def info(self):
		return "Font.  Name: " + str(self.fontName) + ", size: " + str(self.size)


