from nObject import nObject

class nGap(nObject):
	hasRange = False
	mandatoryAttr = ["width", "height"]
	stringAttr = []
	colorAttr = []
	flags = []
	nandeckEnums = ["ON", "OFF"]
	nandeckString = "GAP"
	nObjectType = "gap"

	def __init__(self, deck, width=None, height=None, guidelines=None, preset=None):
		nObject.__init__(self, locals())

	def info(self):
		result = "Gap between cards of " + str(width) + " by " + str(height) + " inches"
		if self.guidelines is None or self.guidelines == "OFF":
			result += "."
		else:
			result += " with guidelines for cutting."
		return result


