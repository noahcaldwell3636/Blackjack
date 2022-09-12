import TestGUI
from BJdealer import Dealer
import inspect


class my_test(TestGUI.testGUI):

    def test_senario_one(self):
        # dealer starts with all the cards, shuffled
        dealer = Dealer()
        self.assertEquals(inspect.currentframe(), dealer.get_deck_count(), 52)
        print(self.testCases)
  
  
test = my_test()
if __name__ == '__main__':
        test.main()