import unittest

class TestImport(unittest.TestCase):
    def test_import(self):
        import actuator

test_suite = unittest.TestSuite((TestImport('test_import'),))

if __name__ == '__main__':
    unittest.main()
