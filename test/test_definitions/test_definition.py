import unittest

from actuator.application import Application
from actuator.definitions.definition import Definition, _UnboundDefinition, \
                                            _extract, _bind

class TestDefinition(unittest.TestCase):
    def test_definition(self):
        definition = Definition(1, 'a', x=1, y='a')
        self.assertIsInstance(definition, _UnboundDefinition)

    def test_definition_bind(self):
        definition = Definition()

        application = Application()
        definition = definition.bind(application)

        self.assertIsInstance(definition, Definition)
        self.assertEqual(definition.parent, application)

    def test_definition__extract(self):
        first_definition = Definition()
        second_definition = Definition()

        class Test(object):
            x = first_definition
            y = second_definition
            z = True

        self.assertEqual(dict(_extract(Test)), {'x': first_definition,
                                                'y': second_definition})

    def test_definition__bind(self):
        first_definition = Definition()
        second_definition = Definition()
        third_definition = Definition()

        class Test(Application):
            pass

        test = Test()

        _bind(test, (('first_definition', first_definition),
                     ('second_definition', second_definition),
                     ('third_definition', third_definition)))

        self.assertTrue(hasattr(test, 'first_definition'))
        self.assertIsInstance(test.first_definition, Definition)
        self.assertIs(test.first_definition.parent, test)

        self.assertTrue(hasattr(test, 'second_definition'))
        self.assertIsInstance(test.second_definition, Definition)
        self.assertIs(test.second_definition.parent, test)

        self.assertTrue(hasattr(test, 'third_definition'))
        self.assertIsInstance(test.third_definition, Definition)
        self.assertIs(test.third_definition.parent, test)

test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestDefinition)

if __name__ == '__main__':
    unittest.main()
