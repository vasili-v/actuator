import unittest

from actuator.exceptions import Error

class TestExceptions(unittest.TestCase):
    def test_error(self):
        class TestError(Error):
            template = '{name} error.'

        with self.assertRaises(TestError) as ctx:
            raise TestError(name='Test')

        self.assertEqual(str(ctx.exception), 'Test error.')

test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestExceptions)

if __name__ == '__main__':
    unittest.main()
