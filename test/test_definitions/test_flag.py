import unittest

from actuator.exceptions import InvalidFlagValue
from actuator.application import Application
from actuator.definitions.definition import _UnboundDefinition, Undefined
from actuator.definitions.flag import Flag

class TestFlag(unittest.TestCase):
    def __make_flag(self, **kwargs):
        return Flag(**kwargs)(Application(), 'test')

    def test_flag(self):
        flag = Flag('test', presence=False, default=Undefined, nullable=True)
        self.assertIsInstance(flag, _UnboundDefinition)

        application = Application()
        flag = flag(application, 'test_flag')
        self.assertIsInstance(flag, Flag)
        self.assertIs(flag.parent, application)
        self.assertEqual(flag.identifier, 'test_flag')
        self.assertEqual(flag.name, 'test')
        self.assertIs(flag.default, Undefined),
        self.assertTrue(flag.nullable)
        self.assertFalse(flag.presence)

    def test_flag_parse_no_value(self):
        self.assertTrue(self.__make_flag(presence=True).parse(None))

    def test_flag_parse_value(self):
        self.assertTrue(self.__make_flag().parse('yes'))

    def test_flag_parse_json_value(self):
        self.assertTrue(self.__make_flag().parse('"yes"'))

    def test_flag_parse_none_value(self):
        self.assertIs(self.__make_flag(nullable=True).parse('nil'), None)

    def test_flag_parse_json_none_value(self):
        self.assertIs(self.__make_flag(nullable=True).parse('null'), None)

    def test_flag_parse_number_value(self):
        self.assertTrue(self.__make_flag().parse('"-3.14e-15"'))

    def test_flag_parse_json_numer_value(self):
        self.assertTrue(self.__make_flag().parse('5.1'))

    def test_flag_parse_invalid_value(self):
        flag = self.__make_flag()
        with self.assertRaises(InvalidFlagValue) as ctx:
            flag.parse('invalid-flag-value')

        self.assertIn('invalid-flag-value', str(ctx.exception))

    def test_flag_parse_invalid_json_value(self):
        flag = self.__make_flag()
        with self.assertRaises(InvalidFlagValue) as ctx:
            flag.parse('{"invalid-flag-value": true}')

        self.assertIn('{"invalid-flag-value": true}', str(ctx.exception))

test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestFlag)

if __name__ == '__main__':
    unittest.main()
