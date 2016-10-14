import unittest
from sdfi import scheduler, tokenizer
from collections import Counter


class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.test1 = 'texts/test1.txt'
        self.test1_result = [('ansley', 5), ('peduru', 5)]
        self.test2 = 'texts/test2.txt'
        self.test2_result = [('rack', 1), ('space', 1), ('managed', 1),
                             ('security', 1), ('engineering', 1), ('san', 1),
                             ('antonio', 1), ('texas', 1), ('usa', 1)]
        self.zen = 'texts/zen.txt'

    def test_one(self):
        self.assertCountEqual(scheduler([self.test1]), self.test1_result)

    def test_two(self):
        self.assertCountEqual(scheduler([self.test2]), self.test2_result)

    def test_zen(self):
        zen_word_count = Counter()
        zen_contents = open(self.zen, 'r').readlines()
        for line in zen_contents:
            line = tokenizer(line)
            zen_word_count.update(line)
        self.assertCountEqual(scheduler([self.zen]), zen_word_count.most_common(10))
