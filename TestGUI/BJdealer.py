from BJcard import Card
from random import seed, shuffle

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
		return len(self.deck)

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
		self.player.update_hand_total()
		# deal self second card
		self.hand.append(self.deck.pop(0))
		self.update_hand_total()


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

	def seeded_shuffle(self, num):	
		seed(num)
		shuffle(self.deck)
		return self.deck


	"""Add player object to the game"""
	def add_player(self, player):
		self.player = player

	"""Award the players money if they won, take theit pot money if
	they lost."""
	def allocate_pot(self):
		pass

	"""Update total of hand. Also updates player's status as well...
	- TODO: figure out the logic if the player is dealt 2 aces, the 
	game currently just says the player's total is 2
	- TODO: seperate this method into two methods: update_total and
	update status"""
	def update_hand_total(self):
		self.hand_total = 0
		# Calculate non-ace cards first
		for card in self.hand:
			if card.value != 'A':
				self.hand_total += card.worth
		for card in self.hand: 
			if card.value == 'A':
				if self.hand_total + 11 > 21:
					card.worth = 1
				self.hand_total += card.worth
		print("")
		print(f"Your total = {self.hand_total}")
		if self.hand_total == 21:
			self.status = "21"
			print("")
			print("You got 21!")
		elif self.hand_total > 21:
			self.status = "busted"
			print("")
			print(f"The dealer with a hand of {self.hand_total}")

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