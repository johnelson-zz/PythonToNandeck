from nObject import nObject

class nCardSize(nObject):
	mandatoryAttr = ["width", "height"]
	nandeckString = "CARDSIZE"
	nObjectType = "cardsize"
	hasRange = False
	defaultWidth = 6
	defaultHeight = 9

	def __init__(self, deck, width=None, height=None, preset=None):
		nObject.__init__(self, locals())

	def defaultPreset(self):
		self.width=nCardSize.defaultWidth
		self.height=nCardSize.defaultHeight

