from nanDeck import *

supplyDataPrefix = "C:\\Users\\John\\Desktop\\nandeck\\output\\catData\\"
supplyData = "\\supply\\"

class supplyImage(nImage):

	def supplyPreset(self):
		self.x = 0
		self.y = 0
		self.height = 8
		self.width = 8
		self.imageFlags = "P"
		self.imageFile = supplyDataPrefix+supplyData+self.imageFile

class supplyText(nText):

	def supplyPreset(self):
		self.x = 0.1
		self.y = 6
		self.width = 7.8
		self.height = 2
		self.font = nFont(deck=self.deck, fontName="Komika Jam", size=20, style="T", charColor="#000000")

	def extraPreset(self):
		self.x = 0.1
		self.y = 0.5
		self.width = 7.8
		self.height = 1
		self.hAlign = "center"
		self.vAlign = "top"
		self.font = nFont(deck=self.deck, fontName="Komika Jam", size=20, style="T", charColor="#000000")
		
if __name__ == "__main__":
	supplyDeck = deck(name="supplyDeck")

	ss = nCardSize(deck=supplyDeck, width=8, height=8)
	sg = nGap(deck=supplyDeck, width=0.5, height=0.5, guidelines="ON") 

	cFile = csvReader(filename=supplyDataPrefix + "supply.csv")
	col = cFile.getColumnsNames()
	for line in cFile:
		try:
			quantity = line["quantity"]
		except KeyError:
			continue
		for x in range(int(quantity)):
			newCard = card(deck=supplyDeck)
			try:
				newCard.tags.append(line["type"])
			except KeyError:
				pass

	tagToFile = {
		"T" : "t_shape.png",
		"box" : "box.png",
		"post" : "post.png",
		"platform" : "platform.png",
		"hammock" : "hammock.png",
		"left ramp" : "ramp_left.png",
		"right ramp" : "ramp_right.png",
		"ramp" : "ramp_right.png",
		"extra ramp" : "ramp_left.png",
		"toy" : "toy.png",
		"treat" : "treat.png",
		"laser" : "laser.png",
	}

	tagToText = {
		#"treat" : supplyText(deck=supplyDeck, text="Choose one: /13/Move a cat in your tree to a spot that fits its preferences./13/Choose a cat from the Catwalk and add it to a spot in your tree that fits its preferences.", preset="supply"),
		#"laser" : supplyText(deck=supplyDeck, text="Choose a cat in any tree. Move that cat to the Catwalk.", preset="supply"),
		"extra ramp" : supplyText(deck=supplyDeck, text="EXTRA RAMP", preset="extra"),
	}

	for card in supplyDeck.cards:
		#background = supplyImage(deck=supplyDeck, imageFile="supply_background.png", preset="supply")
		#card.features.append(background)
		for tag in card.tags:
			if tag in tagToFile:
				newImage = supplyImage(deck=supplyDeck, imageFile=tagToFile[tag], preset="supply")
				#nObject.x_waitsFor_y(x=newImage, y=background)
				card.features.append(newImage)
			if tag in tagToText:
				newText = tagToText[tag]
				card.features.append(newText)
				try:
					nObject.x_waitsFor_y(x=newText, y=newImage)
				except AttributeError:
					#nObject.x_waitsFor_y(x=newText, y=background) 
					pass

	supplyDeck.makeTheDeck()
			
		
