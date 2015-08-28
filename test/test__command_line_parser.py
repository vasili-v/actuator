import unittest
import os

from actuator._command_line_parser import _CommandLineParser, command_line_script

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
        parser.parse_command_line(['/x/y', '-v', '-b'])
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

test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestCommandLineParser)

if __name__ == '__main__':
    unittest.main()
