import unittest
from sdfi import consolidator


class TestConsolidator(unittest.TestCase):
    def setUp(self):
        self.less_than_ten_words = ['Ansley', 'Peduru', 'Unit', 'Unit', 'Test', 'Ansley', 'Ansley']
        self.con_less_than_ten_words = [('Ansley', 3), ('Unit', 2), ('Peduru', 1), ('Test', 1)]
        self.test_less_than_ten_words = ['']

    def test_less_than_ten_words(self):
        self.assertCountEqual(consolidator(self.less_than_ten_words), self.con_less_than_ten_words)

    def test_more_than_ten_words(self):
        pass
