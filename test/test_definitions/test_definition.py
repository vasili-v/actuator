import unittest

from actuator.exceptions import InvalidDefinitionArguments
from actuator.application import Application
from actuator.definitions.definition import Definition, _UnboundDefinition, \
                                            _extract, _bind, _AutoArgument, \
                                            auto

class TestDefinition(unittest.TestCase):
    def test_definition(self):
        class Test(Definition):
            def __init__(self, a, b, x, y, name=auto):
                super(Test, self).__init__(name)

        definition = Test(1, 'a', x=1, y='a')
        self.assertIsInstance(definition, _UnboundDefinition)
        self.assertEqual(definition.arguments, ((1, 'a'), {'x': 1, 'y': 'a'}))

        self.assertIs(definition.error, None)
        self.assertIsInstance(definition.name, _AutoArgument)
        self.assertEqual(definition.name.identifier, 'name')
        self.assertEqual(definition.name.index, 4)
        self.assertTrue(definition.name.required)
        self.assertIs(definition.name.value, None)

    def test_definition_custom_name(self):
        definition = Definition('test')
        self.assertIsInstance(definition, _UnboundDefinition)
        self.assertEqual(definition.arguments, (('test',), {}))

        self.assertIs(definition.error, None)
        self.assertIsInstance(definition.name, _AutoArgument)
        self.assertEqual(definition.name.identifier, 'name')
        self.assertEqual(definition.name.index, 0)
        self.assertFalse(definition.name.required)
        self.assertIs(definition.name.value, 'test')

    def test_definition_invalid_arguments(self):
        definition = Definition('test', name='test')
        self.assertIsInstance(definition, _UnboundDefinition)
        self.assertEqual(definition.arguments, (('test',), {'name': 'test'}))

        self.assertIsInstance(definition.error, TypeError)
        self.assertFalse(hasattr(definition, 'name'))

    def test_definition__call__(self):
        definition = Definition()

        application = Application()
        definition = definition(application, 'test')

        self.assertIsInstance(definition, Definition)
        self.assertEqual(definition.parent, application)
        self.assertEqual(definition.identifier, 'test')

    def test_definition__call__subclassed(self):
        class MyDefinition(Definition):
            def __init__(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z

        definition = MyDefinition(1, 2, 3)
        application = Application()
        definition = definition(application, 'test')

        self.assertIsInstance(definition, Definition)
        self.assertEqual(definition.parent, application)
        self.assertEqual(definition.identifier, 'test')
        self.assertEqual(definition.x, 1)
        self.assertEqual(definition.y, 2)
        self.assertEqual(definition.z, 3)

    def test_definition__call__error(self):
        definition = Definition('test', name='test')

        application = Application()
        with self.assertRaises(InvalidDefinitionArguments) as ctx:
            definition(application, 'test')

        self.assertIn('test', str(ctx.exception))
        self.assertIn('Application', str(ctx.exception))
        self.assertIn(str(definition.error), str(ctx.exception))

    def test_definition__call__custom_name_with_less_arguments(self):
        class Test(Definition):
            def __init__(self, a, b, x=None, y=None, name=auto, z=None, t=None):
                super(Test, self).__init__(name)

        definition = Test(1, 2)
        self.assertIsInstance(definition, _UnboundDefinition)
        self.assertEqual(definition.arguments, ((1, 2), {}))
        self.assertIsInstance(definition.name, _AutoArgument)
        self.assertEqual(definition.name.index, 4)
        self.assertTrue(definition.name.required)
        definition.name.value = 'custom'

        application = Application()
        definition = definition(application, 'test')
        self.assertIsInstance(definition, Test)
        self.assertEqual(definition.name, 'custom')

    def test_definition__call__custom_name_with_exact_arguments(self):
        class Test(Definition):
            def __init__(self, a, b, x=None, y=None, name=auto, z=None, t=None):
                super(Test, self).__init__(name)

        definition = Test(1, 2, 3, 4)
        self.assertIsInstance(definition, _UnboundDefinition)
        self.assertEqual(definition.arguments, ((1, 2, 3, 4), {}))
        self.assertIsInstance(definition.name, _AutoArgument)
        self.assertEqual(definition.name.index, 4)
        self.assertTrue(definition.name.required)
        definition.name.value = 'custom'

        application = Application()
        definition = definition(application, 'test')
        self.assertIsInstance(definition, Test)
        self.assertEqual(definition.name, 'custom')

    def test_definition__call__custom_name_as_keyword_with_exact_arguments \
        (self):
        class Test(Definition):
            def __init__(self, a, b, x=None, y=None, name=auto, z=None, t=None):
                super(Test, self).__init__(name)

        definition = Test(1, 2, 3, 4, name=auto)
        self.assertIsInstance(definition, _UnboundDefinition)
        self.assertEqual(definition.arguments, ((1, 2, 3, 4), {'name': auto}))
        self.assertIsInstance(definition.name, _AutoArgument)
        self.assertEqual(definition.name.index, 4)
        self.assertTrue(definition.name.required)
        definition.name.value = 'custom'

        application = Application()
        definition = definition(application, 'test')
        self.assertIsInstance(definition, Test)
        self.assertEqual(definition.name, 'custom')

    def test_definition__call__custom_name_with_more_arguments(self):
        class Test(Definition):
            def __init__(self, a, b, x=None, y=None, name=auto, z=None, t=None):
                super(Test, self).__init__(name)

        definition = Test(1, 2, 3, 4, auto, 5, 6)
        self.assertIsInstance(definition, _UnboundDefinition)
        self.assertEqual(definition.arguments, ((1, 2, 3, 4, auto, 5, 6), {}))
        self.assertIsInstance(definition.name, _AutoArgument)
        self.assertEqual(definition.name.index, 4)
        self.assertTrue(definition.name.required)
        definition.name.value = 'custom'

        application = Application()
        definition = definition(application, 'test')
        self.assertIsInstance(definition, Test)
        self.assertEqual(definition.name, 'custom')

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
        third_definition = Definition('custom')

        class Test(Application):
            pass

        test = Test()

        _bind(test, (('first_definition', first_definition),
                     ('second_definition', second_definition),
                     ('third_definition', third_definition)))

        self.assertTrue(hasattr(test, 'first_definition'))
        self.assertIsInstance(test.first_definition, Definition)
        self.assertEqual(test.first_definition.name, 'first-definition')
        self.assertIs(test.first_definition.parent, test)
        self.assertEqual(test.first_definition.identifier, 'first_definition')

        self.assertTrue(hasattr(test, 'second_definition'))
        self.assertIsInstance(test.second_definition, Definition)
        self.assertEqual(test.second_definition.name, 'second-definition')
        self.assertIs(test.second_definition.parent, test)
        self.assertEqual(test.second_definition.identifier,
                         'second_definition')

        self.assertTrue(hasattr(test, 'third_definition'))
        self.assertIsInstance(test.third_definition, Definition)
        self.assertEqual(test.third_definition.name, 'custom')
        self.assertIs(test.third_definition.parent, test)
        self.assertEqual(test.third_definition.identifier, 'third_definition')

test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestDefinition)

if __name__ == '__main__':
    unittest.main()
