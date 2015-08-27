import unittest

from actuator.application import Application
from actuator.definitions.definition import _UnboundDefinition
from actuator.definitions.flag import Flag

class TestFlag(unittest.TestCase):
    def test_flag(self):
        flag = Flag('test')
        self.assertIsInstance(flag, _UnboundDefinition)

        application = Application()
        flag = flag(application, 'test_flag')
        self.assertIsInstance(flag, Flag)
        self.assertIs(flag.parent, application)
        self.assertEqual(flag.identifier, 'test_flag')
        self.assertEqual(flag.name, 'test')

test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestFlag)

if __name__ == '__main__':
    unittest.main()
