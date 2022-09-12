import TestGUI
from BJdealer import Dealer
import inspect


class my_test(TestGUI.testGUI):
    def __init__(self):
        super().__init__()


    def test_senario_one(self):
        # dealer starts with all the cards, shuffled
        dealer = Dealer()
        self.assertEquals(inspect.currentframe(), len(dealer.get_deck()), 52)
        print(self.testCases)
  
  
test = my_test()
if __name__ == '__main__':
        test.main()