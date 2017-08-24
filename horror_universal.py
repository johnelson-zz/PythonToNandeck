from nanDeck import *

cardBorder = 0.5
cardWidth = 6
cardHeight = 9
cardWorkingHeight = cardHeight - (2*cardBorder)
cardWorkingWidth = cardWidth - (2*cardBorder)

class banner(nRect):
	bannerX = cardBorder
	bannerY = cardBorder
	bannerWidth = cardWorkingWidth
	bannerHeight = 1.25 
	outlineThickness = 0.05

	def bannerPreset(self):
		self.x=banner.bannerX
		self.y=banner.bannerY
		self.width=banner.bannerWidth
		self.height=banner.bannerHeight
		self.thickness=banner.outlineThickness

class typeText(nText):

	margin = 0.1
	x = cardBorder
	y = cardBorder + margin
	height = banner.bannerHeight - (2*margin)
	width = cardWorkingWidth
	hAlign = "center"
	vAlign = "bottom"

	def typeTextPreset(self):
		self.x=typeText.x
		self.y=typeText.y
		self.width=typeText.width
		self.height=typeText.height
		self.hAlign=typeText.hAlign
		self.vAlign=typeText.vAlign

class hClass(object):

	width = cardWorkingWidth
	height = banner.bannerHeight
	x = cardBorder
	y = cardWorkingHeight - height + cardBorder 
	hAlign = "center"
	vAlign = "bottom"

	def __init__(self):
		pass

class square(object):
	margin = 0.1
	width = .75
	height = .75
	yIncr = height + margin
	x = cardBorder
	startingY = hClass.y - height
	textX = x+width + margin
	textWidth = cardWorkingWidth
	textHeight = yIncr

	def __init__(self):
		pass

	@staticmethod
	def y(which):
		if which <= 1:
			return square.startingY
		else:
			return square.startingY + (square.yIncr*(which-1))

class rulesText(nText):
	x = cardBorder
	y = cardBorder + banner.bannerHeight + .25
	width = cardWorkingWidth
	height = hClass.y - y
	hAlign = "left"
	vAlign = "wordwrap"

	def rulesPreset(self):
		self.x=rulesText.x
		self.y=rulesText.y
		self.width=rulesText.width
		self.height=rulesText.height
		self.hAlign=rulesText.hAlign
		self.vAlign=rulesText.vAlign


class horrorDeck(deck):

	def __init__(self, name):
		deck.__init__(self, name)

		self.horrorColors = {
			
			"think" : "#3333FF",
			"skill" : "#606060",
			"fight" : "#FF0000",
			"move"  : "#00FF00",
			"twitch": "#FFFF00",
			"death" : "#000000",
			"magic" : "#6600CC",
			"white" : "#FFFFFF",
			"black" : "#000000",
			"border": "#000000",
		}

		self.basicStates = ["think", "skill", "fight", "move", "twitch"]
		self.allStates = ["think", "skill", "fight", "move", "twitch", "death", "magic"]
		self.darkStates = ["death"]
		self.cardTypes = ["action", "override", "react"]

		self.whiteTitleFont = nFont(deck=self, fontName="Arial", size=24, style="T", charColor=self.horrorColors["white"]) 
		self.blackTitleFont = nFont(deck=self, fontName="Arial", size=24, style="T", charColor=self.horrorColors["black"]) 
		self.rulesFont = nFont(deck=self, fontName="Arial", size=12, style="T", charColor=self.horrorColors["black"])
		self.stateFont = nFont(deck=self, fontName="Arial", size=10, style="T", charColor=self.horrorColors["black"])

		#this follows a different naming convention so the add banners function works
		self.black_action   = typeText(deck=self, font=self.blackTitleFont, text="Action", preset="typeText" )
		self.white_action   = typeText(deck=self, font=self.whiteTitleFont, text="Action", preset="typeText" )
		self.black_override = typeText(deck=self, font=self.blackTitleFont, text="Override", preset="typeText" )
		self.white_override = typeText(deck=self, font=self.whiteTitleFont, text="Override", preset="typeText" )
		self.black_react    = typeText(deck=self, font=self.blackTitleFont, text="React", preset="typeText" )
		self.white_react    = typeText(deck=self, font=self.whiteTitleFont, text="React", preset="typeText" )

	def produceBanner(self, color, innerColor=None):
		if innerColor is None:
			innerColor = color
		return banner(deck=self, preset="banner", htmlColorBorder=self.horrorColors[color], htmlColorInner=self.horrorColors[innerColor])

	def addBanners(self):
		for c in self.cards:
			cardType = None
			cardState = None
			#print "looking at card with tags: " + str(c.tags)
			for t in c.tags:
				#print "comparing " + str(t) + " to " + str(self.cardTypes)
				if t in self.cardTypes:
					cardType = t
					continue	
				#print "comparing " + str(t) + " to " + str(self.allStates)
				if t in self.allStates:
					cardState = t
					continue
			if cardState is not None:
				c.features.append(self.produceBanner(cardState))
				if cardType is not None:
					textName =  "black" if cardState in self.darkStates else "white"
					textName += "_" + cardType
					#print "TextName = " + str(textName)
					c.features.append(getattr(self, textName))
				else: 
					print "card had state " + str(cardState) + " but no type"
			else:
				print "card had no state"

