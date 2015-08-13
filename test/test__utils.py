import unittest

from actuator._utils import _initialize_class

class Test_Utils(unittest.TestCase):
    def test__initialize_class(self):
        checkpoints = {'init': False, 'self': None}
        class Test(object):
            def __init__(self):
                checkpoints['init'] = True
                checkpoints['self'] = self

        test = Test.__new__(Test)
        _initialize_class(test, tuple(), dict())

        self.assertTrue(checkpoints['init'])
        self.assertIs(checkpoints['self'], test)

    def test__initialize_class_failure(self):
        checkpoints = {'init': False, 'self': None}
        class Test(object):
            def __init__(self):
                checkpoints['init'] = True
                checkpoints['self'] = self
                return False

        test = Test.__new__(Test)
        with self.assertRaises(TypeError) as ctx:
            _initialize_class(test, tuple(), dict())

        self.assertIn(type(False).__name__, str(ctx.exception))
        self.assertTrue(checkpoints['init'])
        self.assertIs(checkpoints['self'], test)

test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(Test_Utils)

if __name__ == '__main__':
    unittest.main()
