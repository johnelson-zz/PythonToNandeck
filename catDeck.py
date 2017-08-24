from nanDeck import *

catDataPrefix = "C:\\Users\\John\\Desktop\\nandeck\\output\\catData\\"
catData = "\\cats\\"
iconData = "\\icons\\"
prefData = "\\preferences\\"

class catText(nText):

	catFont = None
	variableTextSize = False

	def customInit(self):
		catText.bigCatFont = nFont(deck=self.deck, fontName="Komika Jam", size=20, style="T", charColor="#000000")
		catText.medCatFont = nFont(deck=self.deck, fontName="Komika Jam", size=16, style="T", charColor="#000000")
		catText.smallCatFont = nFont(deck=self.deck, fontName="Komika Jam", size=12, style="T", charColor="#000000")
		pass

	def favorPreset(self):
		self.x = 0.1
		self.y = 0.1
		self.height = .5
		self.width = .5
		self.hAlign = "center"
		self.vAlign = "wordwrap"
		self.font = catText.catFont

	def vpPreset(self):
		self.x = 3.4
		self.y = 0.025
		self.height = .5
		self.width = .5
		self.hAlign = "center"
		self.vAlign = "wordwrap"
		self.font = catText.catFont

	def namePreset(self):
		self.x = 0
		self.y = 0.025
		self.height = 0.025+1
		self.width = 4
		self.hAlign = "center"
		self.vAlign = "center"
		if catText.variableTextSize:
			if len(self.text) <= 5:
				self.font = nFont(deck=self.deck, fontName="Komika Jam", size=20, style="T", charColor="#000000")
			elif len(self.text) <= 7:
				self.font = nFont(deck=self.deck, fontName="Komika Jam", size=16, style="T", charColor="#000000")
			elif len(self.text) <= 9:
				self.font = nFont(deck=self.deck, fontName="Komika Jam", size=14, style="T", charColor="#000000")
			else:
				self.font = nFont(deck=self.deck, fontName="Komika Jam", size=11, style="T", charColor="#000000")
		else:
			self.font = nFont(deck=self.deck, fontName="Komika Jam", size=11, style="T", charColor="#000000")

class catImage(nImage):

	iconHeight = 1 
	iconWidth = 1 
	iconMargin = 0.025
	prefHeight = 1
	prefWidth = 1
	prefVMargin = .05
	prefHMargin = .1

	def catPreset(self):
		self.y = catImage.iconHeight + catImage.iconMargin
		self.x = 0
		self.height = 4 -(catImage.iconHeight+catImage.iconMargin+catImage.prefHeight)
		self.width = 4
		self.imageFlags = "TP"
		nObject.x_waitsFor_y(x=self, y=self.deck.backgroundImage)

	def favorPreset(self):
		self.x = catImage.iconMargin
		self.y = catImage.iconMargin
		self.height = catImage.iconHeight
		self.width = catImage.iconWidth
		self.imageFlags = "TP"
		nObject.x_waitsFor_y(x=self, y=self.deck.backgroundImage)

	def vpPreset(self):
		self.x = 4 - catImage.iconWidth
		self.y = catImage.iconMargin
		self.height = catImage.iconHeight
		self.width = catImage.iconWidth
		self.imageFlags = "TP"
		nObject.x_waitsFor_y(x=self, y=self.deck.backgroundImage)

	def prefPreset(self):
		self.y = 4 - catImage.prefVMargin - catImage.prefHeight
		self.height = catImage.prefHeight
		self.width = catImage.prefWidth
		self.imageFlags = "TP"
		nObject.x_waitsFor_y(x=self, y=self.deck.backgroundImage)

	def backgroundPreset(self):
		self.x = 0
		self.y = 0
		self.height = 4
		self.width = 4
	
class CatDeck(deck):

	def customInit(self):
		self.backgroundImage = catImage(deck=self, imageFile=catDataPrefix+catData+"cat_tile_background.png", preset="background")


class catCard(card):

	def customInit(self):
		self.preferences = []
		self.features.append(self.deck.backgroundImage)

if __name__ == "__main__":
	catDeck = CatDeck(name="catDeck")

	cs = nCardSize(deck=catDeck, width=4, height=4)
	cg = nGap(deck=catDeck, width=0.5, height=0.5, guidelines="ON") 

	cFile = csvReader(filename=catDataPrefix + "cats.csv")
	col = cFile.getColumnsNames()
	for line in cFile:
		newCard = catCard(deck=catDeck)
		for c in col:
			newCard.tags.append(str(c) + "_" + str(line[c]))
		#print "newCard.tags: " + str(newCard.tags)

	def stripTagPrefix(lookingIn, found):
		return lookingIn[len(found)+1:]

	def nameFunc(deck, tagPrefix, tagData, card):
		card.features.append(catText(deck=deck, text=tagData, preset=tagPrefix))
		#print "textFunc:"
		#print "deck: " + str(deck) 
		#print "tagPrefix: " + str(tagPrefix)
		#print "tagData: " + str(tagData)
		#print "featureList: " + str(card.features)
		#print "\n"

	def catFunc(deck, tagPrefix, tagData, card):
		imagePrefix = catDataPrefix + catData
		card.features.append(catImage(deck=deck, imageFile=imagePrefix+str(tagData)+".png", preset=tagPrefix))
		#print "imageFunc:"
		#print "deck: " + str(deck) 
		#print "tagPrefix: " + str(tagPrefix)
		#print "tagData: " + str(tagData)
		#print "featureList: " + str(card.features)
		#print "\n"

	def iconFunc(deck, tagPrefix, tagData, card):
		imagePrefix  = catDataPrefix + iconData + tagPrefix
		card.features.append(catImage(deck=deck, imageFile=imagePrefix+str(tagData)+".png", preset=tagPrefix))
		#print "imageFunc:"
		#print "deck: " + str(deck) 
		#print "tagPrefix: " + str(tagPrefix)
		#print "tagData: " + str(tagData)
		#print "featureList: " + str(card.features)
		#print "\n"

	def prefFunc(deck, tagPrefix, tagData, card):
		if len(tagData[2:]):
			card.preferences.append(tagData[2:])

	tagDict = { "name"  : nameFunc,
	            "cat"   : catFunc,
	            "favor" : iconFunc,
	            "vp"    : iconFunc,
		    "pref"  : prefFunc}

	#this dict should be in all lower case, but the inputs aren't sensitive
	prefDict = { 
	             "1 higher" :	"pref_1_higher.png",
	             "1 lower"  :	"pref_1_lower.png",
	             "2 higher" :	"pref_2_higher.png",
	             "2 lower"  :	"pref_2_lower.png",
	             "3 higher" :	"pref_3_higher.png",
	             "3 lower"  :	"pref_3_lower.png",
	             "4 higher" :	"pref_4_higher.png",
	             "4 lower"  :	"pref_4_lower.png",
	             "5 higher" :	"pref_5_higher.png",
	             "5 lower"  :	"pref_5_lower.png",
	             "low" 	:	"pref_2_lower.png",
	             "high"	:	"pref_3_higher.png",
	             "level 5"	:	"pref_5_higher.png",
	             "box"	:	"pref_box.png",
	             "no box"	:	"pref_no_box.png",
	             "post"	:	"pref_post.png",
	             "no post"	:	"pref_no_post.png",
	             "toy"	:	"pref_toy.png",
	             "hammock"	:	"pref_hammock.png",
	             "ramp"	:	"pref_ramp.png",
	             "platform" :	"pref_platform.png",
	             "0 cat"	:	"pref_no_cat.png",
	             "1 cat"	:	"pref_cat_1.png",
	             "2 cat"	:	"pref_cat_2.png",
	             "3 cat"	:	"pref_cat_3.png",
	             "4 cat"	:	"pref_cat_4.png",
	             "5 cat"	:	"pref_cat_5.png",
	             "1+ cat"	:	"pref_cat_1_plus.png",
	             "2+ cat"	:	"pref_cat_2_plus.png",
	             "3+ cat"	:	"pref_cat_3_plus.png",
	             "4+ cat"   :	"pref_cat_4_plus.png",
	             "5+ cat"   :	"pref_cat_5_plus.png",
	             "1- cat"	:	"pref_cat_1_minus.png",
	             "2- cat"	:	"pref_cat_2_minus.png",
	             "3- cat"	:	"pref_cat_3_minus.png",
	             "4- cat"	:	"pref_cat_4_minus.png",
	             "5- cat"	:	"pref_cat_5_minus.png",
	             "circle"   :	"pref_circle.png"
	           }

	for card in catDeck.cards:
		for cardTag in card.tags:
			for tagPrefix in tagDict.iterkeys():
				checking = cardTag[:len(tagPrefix)] 
				if checking == tagPrefix:
					tagDict[tagPrefix](deck = catDeck, tagPrefix=tagPrefix, tagData=stripTagPrefix(cardTag, tagPrefix), card=card)

	for card in catDeck.cards:
		if len(card.preferences) == 0:
			continue
		numPref = len(card.preferences)
		horzSpace = numPref * (catImage.prefHMargin + catImage.prefWidth)
		startingX = (4 - horzSpace)/2
		#print "numPref: " + str(numPref)
		for index in range(numPref):
			try:
				prefFile = prefDict[card.preferences[index].lower()]
			except KeyError:
				print "index: " + str(index)
				print "card.preferences: " + str(card.preferences)
				print "Error: Ignoring unknown preference " + str(card.preferences[index])
			else:
				x = startingX + ((catImage.prefHMargin+catImage.prefWidth)*index)
				newPref = catImage(deck=catDeck, imageFile=catDataPrefix+prefData+prefFile, x=x, preset="pref")
				#newPrefCircle = catImage(deck=catDeck, imageFile=catDataPrefix+prefData+prefDict["circle"], x=x, preset="pref")
				#nObject.x_waitsFor_y(x=newPref, y=newPrefCircle)
				card.features.append(newPref)
				#card.features.append(newPrefCircle)
			
		
	catDeck.makeTheDeck()
