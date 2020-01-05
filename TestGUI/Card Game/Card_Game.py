from random import shuffle
from dealer import Dealer
from player import Player


class CardGame:
	def __init__(self):
		self.dealer = None
		self.player = None

	def print_welcome_art(self):
		print("")
		print("")
		print("=======================================================")
		print("=======================================================")
		print("~~~~~~~~~~Welcome to a new round of Blackjack~~~~~~~~~~")
		print("=======================================================")
		print("=======================================================")

	def assign_dealer(self, dealer):
		self.dealer = dealer

	def assign_player(self, player):
		self.player = player


# Set up match
game = CardGame()
dealer = Dealer()
player1 = Player(dealer)
dealer.add_player(player1)
player1.buy_chips(1000)
player1.place_bet(100)

# Begin round
game.print_welcome_art()
dealer.shuffle()
dealer.deal_round()
print("")
print(f"Your hand = {player1.hand}")
print("")
print(f"Dealer's hand = {dealer.hand}")

# Player one's turn
while player1.status == "playing":
	print("")
	action = input("Would you like to hit or stand? ")
	if action == "hit":
		player1.hit()
	elif action == "stand":
		player1.stand()
print("")
print(f"Player1's hand: {player1.hand}")

# Dealer's turn
print("")
print(f"dealer's total: {dealer.get_hand_total()}")
while (dealer.get_hand_total() < player1.get_hand_total() 
		and player1.status != "busted"
		and dealer.status != "busted"):
 	dealer.hit()
print("")
print(f"dealer's hand = {dealer.hand}")

# who won?
if player1.status == "busted" and dealer.status == "busted":
	print("")
	print("the dealer and player both busted, this should\
		be impossible in b lackjack")
elif player1.status == "busted":
	print("")
	print("player busted. The dealer wins.")
elif dealer.status == "busted":
	print("")
	print("Dealer busted. The player wins.")
	print("")
elif dealer.get_hand_total() > player1.get_hand_total():
	print("")
	print("Dealer has a higher hand. Dealer wins.")
	print("")
elif dealer.get_hand_total() < player1.get_hand_total():
	print("")
	print("Player has a higher hand. Player wins.")
	print("")
else:
	print("")
	print("there has been an overlooked case, who won?")
	print("")

# dealer.allocate_pot()