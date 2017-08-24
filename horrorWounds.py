from nanDeck import *
from horror_universal import *

if __name__ == "__main__":

	woundDeck = horrorDeck(name="woundDeck")

	#various texts
	injuryText = "Injury: this card may not be replaced."
	injury = rulesText(deck=woundDeck, font=woundDeck.rulesFont, text=injuryText, preset="rules")

	recoverText= "Recover: when you play this card, return it."
	recover = rulesText(deck=woundDeck, font=woundDeck.rulesFont, text=recoverText, preset="rules")


	numWounds = 60
	numPassiveWounds = numWounds - numWounds/2
	passiveWoundsPerState = numPassiveWounds / len(woundDeck.basicStates)
	woundList = card.generateCards(deck=woundDeck, number=numWounds, tags="wound")
	for x in range(len(woundList)):
		if x < numWounds - numPassiveWounds:
			thisState = woundDeck.basicStates[x/passiveWoundsPerState]
			woundList[x].tags.append("disabling")
			woundList[x].tags.append("override")
			woundList[x].tags.append(thisState)
			if x % passiveWoundsPerState > passiveWoundsPerState/2:
				woundList[x].tags.append("recoverable")
		else:
			woundList[x].tags.append("passive")
			woundList[x].tags.append("death")
			woundList[x].tags.append("action")

	woundDeck.addBanners()

	for w in woundList:
		if "passive" in w.tags:
			w.features.append(injury)

		if "recoverable" in w.tags:
			w.features.append(recover)
			
	woundDeck.makeTheDeck()	
