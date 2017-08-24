Python classes that write nandeck files for you.

These python classes allow you to access all of the features of nanDeck without having to learn nanDeck syntax. Each supported nanDeck command has a corresponding class. All of these inherit from nObject (nanDeck object). The parameters of nObjects follow the parameters of the nanDeck command they implement as closely as possible. There are two extra parameters on each nObject:

The first is deck. The deck class is a container that holds cards, which have features (nObjects). When you make an nObject, you must initialize it with a deck. If you want that nObject has a range, you need to add it to the feature lists of cards in that deck. Once you've done that and called MakeTheDeck, the deck will calculate all of the ranges and the order of the commands for you.

The second is preset. Any nObject initialized with a preset value will attempt to call the corresponding preset function. For example, an nObject initialized with preset="bacon" will go through its normal constructor and then call self.baconPreset(). This allows you to easily create classes that extend nObjects in the ways they're most often used in your deck.

Cards have 2 attributes that should be messed with - features and tags. "tags" is a list into which you can put anything you want. Tags don't do anything by themselves, they're just an easy way to organize cards. In a standard 52 card deck, you might tag the first 13 cards as "hearts", then the next 13 as "diamonds", etc, and then go back and add number tags '1', '2', '3'...'king' later.

yourCard.features is a class that, from the outside, should act exactly like a list. Features keeps track of all nObjects that will be on a particular card. The special class exists to implement "addsOn," an attribute of nObject that can be set so that nObjects of the same nObjectType will combine with each other. If you have a RuleText class that extends nText, for example, you might set addsOn so that multiple instances of RulesText merge with each other.

To order commands relative to each other, use nObject.x_waitsFor_y or nObject.x_waitsForDirectly_y.

x_waitsFor_y means x will not happen until y has already happened. This is good for text that has to go in front of an image, or backgrounds to cards, etc.

x_waitsForDirectly_y means x will happen after y but before any nObject of y's general type. "General type" refers to the nObjectType attribute, which is used to keep track of the type at a more abstract level than the class. That is, if you create several classes that inherit from nFont, they're still all Fonts and therefore should still all have the "font" nObjectType. So, for example, when you create a text that must have a certain type of font, that's exactly the situation x_waitsForDirectly_y was created for: you can be sure the x (the text) will occure after the font (the y) and before any other font.

The x_waitsForDirectly_y relationship with texts and fonts is already done automatically; if there's always a relationship like this, the class file of the nandeck command should handle it automatically. As much as possible, the user should not need to know how nanDeck works to use the commands.

The only import statement that should ever be needed is "from nanDeck.py import *"