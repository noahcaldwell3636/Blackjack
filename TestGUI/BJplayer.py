"""
- Player class
"""
class Player:
	
	"""Initailize player object"""
	def __init__(self, dealer):
		self.bankroll = 0
		self.hand = [] #hand of card objects
		self.total = 0
		self.current_bet = 0
		self.status = "playing"
		self.dealer = dealer

	"""String representation of object"""
	def __repr__(self):
		if len(self.hand) > 0:
			return f"Player with {self.hand}"
		else:
			return "Player with no cards"

	"""Place bet on table for blackjack.
	@param amount - amount the player is betting"""
	def place_bet(self, amount):
		self.current_bet += amount
		self.bankroll -= amount

	"""Returns the cards the player currently posses."""
	def get_hand(self):
		return self.hand

	"""Get the amount the players cards add up to according to blackjack 
	rules. Aces need to be accounted for correctly as they can be either
	a value of one or eleven."""
	def get_hand_total(self):
		return self.total

	"""Player will finish the round with his current hand"""
	def stand(self):
		if self.status == "21" or "busted":
			self.status = "stand"
			print("")
			print("Player stands")

	"""Player requests another card from dealer."""
	def hit(self):
		card = self.dealer.deck.pop(0)
		self.hand.append(card)
		print("")
		print(f"The player hit and got {card}")
		self.update_total()

	"""Buy the amount of money the player will have to bet.
	@param amount - The amount of money the player wants to buy."""	
	def buy_chips(self, amount):
		self.bankroll += amount

	"""Update total of hand. Also updates player's status as well...
	- TODO: figure out the logic if the player is dealt 2 aces, the 
	game currently just says the player's total is 2
	- TODO: seperate this method into two methods: update_total and
	update status"""
	def update_total(self):
		self.total = 0
		# Calculate non-ace cards first
		for card in self.hand:
			if card.value != 'A':
				self.total += card.worth
		for card in self.hand: 
			if card.value == 'A':
				if self.total + 11 > 21:
					card.worth = 1
				self.total += card.worth
		print("")
		print(f"Your total = {self.total}")
		if self.total == 21:
			self.status = "21"
			print("")
			print("You got 21!")
		elif self.total > 21:
			self.status = "busted"
			print("")
			print(f"The you busted with a hand of {self.total}")

