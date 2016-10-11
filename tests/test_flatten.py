import unittest
from sdfi import flatten


class TestFlatten(unittest.TestCase):
    def setUp(self):
        self.multiple_lists = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.flat_multiple_lists = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.single_list = [[1, 2, 3, 4, 5], []]
        self.flat_single_list = [1, 2, 3, 4, 5]

    def test_empty(self):
        self.assertEqual(flatten([]), [])
        self.assertEqual(flatten([[], []]), [])

    def test_single_list(self):
        self.assertEqual(flatten(self.single_list), self.flat_single_list)

    def test_not_list_of_lists(self):
        with self.assertRaises(TypeError):
            flatten(self.flat_single_list)

    def test_multiple_lists(self):
        self.assertEqual(flatten(self.multiple_lists), self.flat_multiple_lists)
