from nObject import nObject

class nRect(nObject):

	mandatoryAtrr = ["x","y", "width", "height", "htmlColorBorder", "htmlColorInner", "thickness"]
	stringAttr = []
	colorAttr = ["htmlColorBorder", "htmlColorInner"]
	flags = []
	nandeckEnums = []
	nandeckString = "RECTANGLE"
	nObjectType = "rect"

	def __init__(self, deck, cRange=None, x=None, y=None, width=None, height=None, htmlColorBorder=None, htmlColorInner=None, thickness=None, preset=None):
		nObject.__init__(self, locals())

	def info(self):
		return "Rectange. ID: " + str(self.id) + ", Color: " + str(self.htmlColorInner) + ", x: " + str(self.x) + ", y: " + str(self.y) + ", height: " + str(self.height) + ", width:" + str(self.width)


	def preValidateAdjust(self):
		if self.htmlColorInner is None:
			self.htmlColorInner = self.htmlColorBorder


