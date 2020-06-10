import unittest
from part1 import *

class TestShuffleInNew(unittest.TestCase):

    def setUp(self):
        self.cards = list(range(10))
        self.size = len(self.cards)

    def test_Shuffles(self):
        final = reversed(self.cards)
        for pos, value in enumerate(final):
            with self.subTest(pos=pos):
                calc = reverse_deal_into_new_stack(self.size, pos)
                self.assertEqual(value, self.cards[calc])

    def test_cuts(self):
        for cut in range(-9,10):
            final = self.cards[cut:] + self.cards[:cut] 
            for pos, value in enumerate(final):
                calc = reverse_cuts(self.size, pos, cut)
                with self.subTest(cut=cut, pos=pos, position=calc, final=final):
                    self.assertEqual(value, self.cards[calc])

    
if __name__ == '__main__':
    unittest.main()