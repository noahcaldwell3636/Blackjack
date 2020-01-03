import TestGUI
from Card_Game import Dealer
import inspect


class my_test(TestGUI.testGUI):
	def __init__(self):
		super().__init__()


	def test_senario_one(self):
		# dealer starts with all the cards, shuffled
		dealer = Dealer()
		self.assertEquals(inspect.currentframe(), dealer.count(), 52)

		# player places a bet from bankroll

		# dealer deals cards to player and himself
			# dealer has a 5D and JS
			# dealer has 16 total
			# player has a 9D and 4D
			# player has 13 total

		# player hits until he busts
			# player hits, gets 5H
			# player has 18 total
			# player hits, gets 4S
			# player has 22
			# player busts

		# dealer takes bet from player

		# round over




test = my_test()
if __name__ == '__main__':
		test.main()