import unittest

import test_definition
import test_flag

test_suite = unittest.TestSuite((test_definition.test_suite,
                                 test_flag.test_suite))

if __name__ == '__main__':
    unittest.main()
