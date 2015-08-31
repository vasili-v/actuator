import unittest
import os

from actuator.exceptions import UnrecognizedApplicationArgument
from actuator.definitions.definition import Definition
from actuator._command_line_parser import _CommandLineParser, command_line_script
from actuator.application import Application

class TestCommandLineParser(unittest.TestCase):
    def setUp(self):
        self.__isfile = os.path.isfile
        self.__isdir = os.path.isdir

    def tearDown(self):
        os.path.isdir = self.__isdir
        os.path.isfile = self.__isfile

    def test_command_line_parser_parse_command_line(self):
        def isfile(path):
            return path == '/x/y'

        os.path.isfile = isfile

        def isdir(path):
            return path == '/x'

        os.path.isdir = isdir

        parser = _CommandLineParser()
        parser.parse_command_line(['/x/y'])
        self.assertEqual(parser.actuator_executable, '/x/y')
        self.assertEqual(parser.actuator_executable_directory, '/x')
        self.assertEqual(parser.actuator_executable_name, 'y')

    def test_command_line_parser_parse_command_line_empty(self):
        parser = _CommandLineParser()
        parser.parse_command_line([])
        self.assertIs(parser.actuator_executable, None)
        self.assertIs(parser.actuator_executable_directory, None)
        self.assertIs(parser.actuator_executable_name, None)

    def test_command_line_parser_parse_executable_path_empty(self):
        parser = _CommandLineParser()
        parser.parse_executable_path('')
        self.assertIs(parser.actuator_executable, None)
        self.assertIs(parser.actuator_executable_directory, None)
        self.assertIs(parser.actuator_executable_name, None)

    def test_command_line_parser_parse_executable_path_command_line_script(self):
        def isfile(path):
            return False

        os.path.isfile = isfile

        parser = _CommandLineParser()
        parser.parse_executable_path('-c')
        self.assertIs(parser.actuator_executable, command_line_script)
        self.assertIs(parser.actuator_executable_directory, None)
        self.assertIs(parser.actuator_executable_name, None)

    def test_command_line_parser_parse_executable_path(self):
        def isfile(path):
            return path == '/x/y'

        os.path.isfile = isfile

        def isdir(path):
            return path == '/x'

        os.path.isdir = isdir

        parser = _CommandLineParser()
        parser.parse_executable_path('/x/y')
        self.assertEqual(parser.actuator_executable, '/x/y')
        self.assertEqual(parser.actuator_executable_directory, '/x')
        self.assertEqual(parser.actuator_executable_name, 'y')

    def test_command_line_parser_parse_executable_path_no_dir(self):
        def isfile(path):
            return path == '/x/y'

        os.path.isfile = isfile

        def isdir(path):
            return False

        os.path.isdir = isdir

        parser = _CommandLineParser()
        parser.parse_executable_path('/x/y')
        self.assertEqual(parser.actuator_executable, '/x/y')
        self.assertIs(parser.actuator_executable_directory, None)
        self.assertEqual(parser.actuator_executable_name, 'y')

    def test_command_line_parser_parse_named_argument(self):
        class Test(object):
             identifier = 'test'

             def parse(self, value):
                 return value

        names = {'test': Test()}

        parser = _CommandLineParser()
        parser.parse_named_argument('test=value', names)
        self.assertEqual(parser.test, 'value')

    def test_command_line_parser_parse_named_argument_no_value(self):
        class Test(object):
             identifier = 'test'

             def parse(self, value):
                 return value

        names = {'test': Test()}

        parser = _CommandLineParser()
        parser.parse_named_argument('test', names)
        self.assertIs(parser.test, None)

    def test_command_line_parser_parse_named_argument_no_value(self):
        parser = _CommandLineParser()
        with self.assertRaises(UnrecognizedApplicationArgument) as ctx:
            parser.parse_named_argument('unknown', {})

        self.assertIn('unknown', str(ctx.exception))
        self.assertIn('_CommandLineParser', str(ctx.exception))

    def test_command_line_parser_parse_command_line_arguments(self):
        class TestDefinition(Definition):
            def parse(self, value):
                return value

        parser = Application()
        parser.first = TestDefinition('first')(parser, 'first')
        parser.second = TestDefinition('second')(parser, 'second')
        parser.third = TestDefinition('third')(parser, 'third')

        parser.parse_command_line_arguments(('--first=first_value',
                                             '--second=second_value',
                                             '--third=third_value'))

        self.assertEqual(parser.first, 'first_value')
        self.assertEqual(parser.second, 'second_value')
        self.assertEqual(parser.third, 'third_value')

    def test_command_line_parser_parse_command_line_arguments_unknown_argument(self):
        parser = _CommandLineParser()

        with self.assertRaises(UnrecognizedApplicationArgument) as ctx:
            parser.parse_command_line_arguments(('unknown',))

        print str(ctx.exception)
        self.assertIn('unknown', str(ctx.exception))
        self.assertIn('_CommandLineParser', str(ctx.exception))

test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestCommandLineParser)

if __name__ == '__main__':
    unittest.main()
