import unittest

from actuator.application import Application
from actuator.definitions.definition import Definition, _UnboundDefinition

class TestDefinition(unittest.TestCase):
    def test_definition(self):
        definition = Definition(1, 'a', x=1, y='a')
        self.assertIsInstance(definition, _UnboundDefinition)

    def test_definition_make(self):
        definition = Definition()

        application = Application()
        definition = definition.make(application)

        self.assertIsInstance(definition, Definition)
        self.assertEqual(definition.parent, application)

test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestDefinition)

if __name__ == '__main__':
    unittest.main()
