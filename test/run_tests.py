import sys
import unittest

test_modules = ["test_sample", "test_data_loader"]

suite = unittest.TestSuite()

for t in test_modules:
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

result = not unittest.TextTestRunner().run(suite).wasSuccessful()
sys.exit(result) # Throw exit code 1 if tests failed