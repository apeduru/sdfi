import unittest
from sdfi import scheduler, tokenizer
import re
from collections import Counter


class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.test1 = 'texts/test1.txt'
        self.test1_result = [('Ansley', 1), ('Peduru', 1)]
        self.test2 = 'texts/test2.txt'
        self.test2_result = [('Rack', 1), ('Space', 1), ('Managed', 1),
                             ('Security', 1), ('Engineering', 1), ('San', 1),
                             ('Antonio', 1), ('Texas', 1), ('USA', 1)]
        self.zen = 'texts/zen.txt'

    def test_one(self):
        self.assertCountEqual(scheduler([self.test1]), self.test1_result)

    def test_two(self):
        self.assertCountEqual(scheduler([self.test2]), self.test2_result)

    def test_zen(self):
        zen_word_count = Counter()
        zen_contents = open(self.zen, 'r').readlines()
        for line in zen_contents:
            line = list(filter(None, tokenizer(line)))
            zen_word_count.update(line)
        self.assertCountEqual(scheduler([self.zen]), zen_word_count.most_common(10))
