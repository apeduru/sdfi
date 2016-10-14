import unittest
from sdfi import tokenizer


class TestTokenizer(unittest.TestCase):
    def setUp(self):
        self.short_string = "Ansley"
        self.long_string = "The quick brown fox jumps over the lazy dog"
        self.tokenized_long_string = ["the", "quick", "brown", "fox", "jumps",\
                                      "over", "the", "lazy", "dog"]
        self.character_string = "\t !! %&$$\n"
        self.number_string = "1000 99 1996 911"
        self.tokenized_number_string = ["1000", "99", "1996", "911"]

    def test_no_string(self):
        self.assertEqual(tokenizer(''), [])

    def test_short_string(self):
        self.assertEqual(tokenizer(self.short_string), [self.short_string.lower()])

    def test_long_string(self):
        self.assertEqual(tokenizer(self.long_string), self.tokenized_long_string)

    def test_character_string(self):
        self.assertEqual(tokenizer(self.character_string), [])

    def test_number_string(self):
        self.assertEqual(tokenizer(self.number_string), self.tokenized_number_string)
