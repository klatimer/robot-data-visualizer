import sys
import unittest

test_modules = ["test_data_loader", "test_data_manager", "test_get_dates_umich", "test_download_tar", "test_tar_extract"]

suite = unittest.TestSuite()

for t in test_modules:
    print("adding tests in \"" + t + "\"")
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

result = not unittest.TextTestRunner().run(suite).wasSuccessful()
sys.exit(result) # Throw exit code 1 if tests failed