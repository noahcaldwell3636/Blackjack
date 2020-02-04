from BJcard import Card
from random import shuffle

""" 
- Handles the game's deck
"""
class Dealer:
	
	"""Initialize dealer object"""
	def __init__(self):
		suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
		values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
		self.deck = [Card(suit, value) for suit in suits for value in values]
		self.player = None
		self.hand = []
		self.hand_total = 0
		self.status = "playing"

	"""String representation of the dealer"""
	def __repr__(self):
		return f"Deck of {self.get_deck_count()} Cards"

	"""Returns a list of cards that make up the dealer's deck."""
	def get_deck(self):
		return self.deck

	"""Returns the amount of cards the dealer's deck."""
	def  get_deck_count(self):
		count = 0
		for card in self.deck:
			count += 1
		return count

	"""Get the combined value of the dealer's hand in accordinance with
	the rules of blackjack"""
	def get_hand_total(self):
		return self.hand_total

	"""deals 2 cards to self and 2 cards to every player in the game"""
	def deal_round(self):
		# clear table
		self.player.hand.clear()
		self.hand.clear()
		# deal player the first card
		self.player.hand.append(self.deck.pop(0))
		# deal self first card
		self.hand.append(self.deck.pop(0))
		# deal player second card
		self.player.hand.append(self.deck.pop(0))
		self.player.update_total()
		# deal self second card
		self.hand.append(self.deck.pop(0))
		self.update_total()


	"""Deal player a card"""
	def deal(self, player, amount=1):
		for i in range(amount):
			player.hand.append(self.deck.pop(0))


	"""Shuffle the deck of cards in a new order"""
	def shuffle(self):
		if self.get_deck_count() != 52:
			raise ValueError("Only full decks can be shuffled")
		else:
			shuffle(self.deck)
			return self.deck

	"""Add player object to the game"""
	def add_player(self, player):
		self.player = player

	"""Award the players money if they won, take theit pot money if
	they lost."""
	def allocate_pot(self):
		pass

	"""Tallys up the combined total of the cards in the dealer's hand
	and update the hand_total attribute. Should be called everytime
	their is a change to the player's hand.
	- TODO: figure out the logic if the player is dealt 2 aces, the 
	game currently just says the player's total is 2"""
	def update_hand_total(self):
		self.hand_total = 0
		for card in self.hand:
			if card.value == "A" and self.get_hand_total() <= 11:
				card.worth = 1
			self.hand_total += card.worth
		if self.hand_total > 21:
			self.status = "busted"
			print("the dealer busted")

	"""Add a card from the deck to the dealer's hand"""
	def hit(self):
		card = self.deck.pop(0)
		self.hand.append(card)
		print(f"The Dealer hit and got a {card}")
		self.update_hand_total()
		print(f"dealers total: {self.hand_total}")

	"""Update total of hand.
	- TODO: figure out the logic if the player is dealt 2 aces, the 
	game currently just says the player's total is 2"""
	def update_total(self):
		self.total = 0
		for card in self.hand:
			if card.value == "A" and self.get_hand_total() <= 11:
				card.worth = 1
			self.total += card.worth
		print("")
		print(f"Dealer's total = {self.total}")
		if self.total == 21:
			self.status = "21"
			print("")
			print("You got 21!")
		elif self.total > 21:
			self.status = "busted"
			print("")
			print(f"The you busted with a hand of {self.total}")