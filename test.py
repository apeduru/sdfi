import unittest
from tests import test_flatten, test_tokenizer, test_consolidator, test_scheduler

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTest(loader.loadTestsFromModule(test_flatten))
suite.addTest(loader.loadTestsFromModule(test_consolidator))
suite.addTest(loader.loadTestsFromModule(test_tokenizer))
suite.addTest(loader.loadTestsFromModule(test_scheduler))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
