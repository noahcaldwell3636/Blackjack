import TestGUI
from Card_Game import Dealer
import inspect


class my_test(TestGUI.testGUI):
	def __init__(self):
		super().__init__()
		self.dealer = Dealer()

	def test_count(self):
		self.assertEquals(inspect.currentframe(), self.dealer.count(), 52)

	def test_count_fail(self):
		self.assertEquals(inspect.currentframe(), self.dealer.count(), 512)

	def test_repr(self):
		self.assertEquals(inspect.currentframe(), self.dealer, "dealer with deck of 47 Cards")

	def test_deal(self):
		self.dealer._deal(5)
		self.assertEquals(inspect.currentframe(), self.dealer.count(), 47)

	def test_not_equal(self):
		self.assertNotEqual(inspect.currentframe(), self.dealer.count(), 40)

	def test_assert_true(self):
		self.assertTrue(inspect.currentframe(), self.dealer.count() == 52)

	def test_assert_false(self):
		self.assertFalse(inspect.currentframe(), self.dealer.count() == 30)

	def test_assert_false_fail(self):
		self.assertFalse(inspect.currentframe(), self.dealer.count() == 52)


test = my_test()
if __name__ == '__main__':
		test.main()