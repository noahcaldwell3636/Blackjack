from random import shuffle
import dealer

# Main
dealer = Dealer()
player = Player()

player.place_bet()
dealer.deal()
player.get_hand()

while player.get_total() <= 17:
	player.hit()
	player.fold()

while dealer.get_total() < player.get_total():
	dealer.hit()

dealer.allocate_pot()