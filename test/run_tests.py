import unittest

test_modules = ["test_sample", "test_data_loader"]

suite = unittest.TestSuite()

for t in test_modules:
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

unittest.TextTestRunner().run(suite)