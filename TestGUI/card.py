"""
- Just a card object
"""
class Card:

	allowed_suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
	allowed_values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

	def __init__(self, suit, value):
		if suit not in Card.allowed_suits:
			raise ValueError(f"{suit} is not a valid suit of {str(Card.allowed_suits)}")
		if value not in Card.allowed_values:
			raise ValueError(f"{value} is not a valid value of {str(Card.allowed_values)}")
		self.suit = suit
		self.value = value

	def __repr__(self):
		return f"{self.value} of {self.suit}"
