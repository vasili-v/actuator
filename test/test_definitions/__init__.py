import unittest

import test_definition

test_suite = unittest.TestSuite((test_definition.test_suite,))

if __name__ == '__main__':
    unittest.main()
