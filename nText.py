from nObject import nObject

class nText(nObject):

	mandatoryAttr = [ "font", "text", "x", "y", "width", "height", "hAlign", "vAlign"]
	stringAttr = ["text"]
	colorAttr = []
	flags = []
	nandeckEnums = ["top", "center", "bottom", "wordwrap", "wwtop", "wwcenter", "wwbottom", "charwrap", "left", "center", "right"]
	nandeckString = "TEXT"
	nObjectType = "text"
	addsOn = False
	maxRound = 1

	def __init__(self, deck, font=None, cRange=None, text=None, x=None, y=None, width=None, height=None, hAlign=None, vAlign=None, angle=None, alpha_channel=None, outline_width=None, cOffset=None, cAngle=None, preset=None):
		nObject.__init__(self, locals())
		#print "constructed text with text " + str(self.text)

	def info(self):
		return "text: " + str(self.text)

	def appendText(self, newText):
		if self.text is None:
			self.text = newText
		else:
			self.text += "\\13\\" + str(value)

	def round1Validation(self, deck):
		message = None
		for font in deck.nObjectTypeDict["font"]:
			if font.equivalent(self.font):
				haveFont = True
				break
		if not haveFont:
			message = "Don't have font for text " + str(text.text)
		return message

	def preValidateAdjust(self):
		self.waitForDirectly.append(self.font)
		self.font.awaitedDirectly.append(self)

