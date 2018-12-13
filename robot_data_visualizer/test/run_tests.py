import sys
import unittest

test_modules = ["test_data_manager", "test_download_tar", "test_get_dates_umich", "test_tar_extract", "test_time_convert", "test_threshold_lidar"]

suite = unittest.TestSuite()

for t in test_modules:
    print("adding tests in \"" + t + "\"")
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

result = not unittest.TextTestRunner().run(suite).wasSuccessful()
sys.exit(result) # Throw exit code 1 if tests failed