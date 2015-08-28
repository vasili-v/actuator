import unittest
import sys
import StringIO

from actuator.exceptions import Error, ApplicationRedefined
from actuator.application import _registry, Application, main, command_line_script
from actuator.definitions.definition import Definition, _UnboundDefinition

class TestApplication(unittest.TestCase):
    def setUp(self):
        self.__stderr = sys.stderr

    def tearDown(self):
        _registry.application = Application
        sys.stderr = self.__stderr

    def test_import(self):
        self.assertEqual(_registry.application, Application)

    def test_application_subclassing(self):
        class TestApplication(Application):
            pass

        self.assertEqual(_registry.application, TestApplication)

    def test_application_second_subclassing(self):
        class TestApplication(Application):
            pass

        self.assertEqual(_registry.application, TestApplication)

        with self.assertRaises(ApplicationRedefined) as ctx:
            class SecondTestApplication(Application):
                pass

        self.assertIn('TestApplication', str(ctx.exception))
        self.assertIn('SecondTestApplication', str(ctx.exception))

    def test_application(self):
        checkpoints = {'new': False, 'cls': None, 'x': None,
                       'init': False, 'self': None}

        class MyApplication(Application):
            x = Definition()

            def __new__(cls):
                checkpoints['new'] = True
                checkpoints['cls'] = cls
                checkpoints['x'] = cls.x
                return super(MyApplication, cls).__new__(cls)

            def __init__(self):
                checkpoints['init'] = True
                checkpoints['self'] = self

        application = MyApplication()

        self.assertTrue(checkpoints['new'])
        self.assertIs(checkpoints['cls'], MyApplication)
        self.assertIsInstance(checkpoints['x'], _UnboundDefinition)

        self.assertTrue(checkpoints['init'])
        self.assertIs(checkpoints['self'], application)

        self.assertIsInstance(application.x, Definition)

    def test_application_new_failure(self):
        checkpoints = {'new': False, 'cls': None, 'x': None,
                       'init': False, 'self': None}

        class MyApplication(Application):
            x = Definition()

            def __new__(cls):
                checkpoints['new'] = True
                checkpoints['cls'] = cls
                checkpoints['x'] = cls.x
                return None

            def __init__(self):
                checkpoints['init'] = True
                checkpoints['self'] = self

        application = MyApplication()

        self.assertTrue(checkpoints['new'])
        self.assertIs(checkpoints['cls'], MyApplication)
        self.assertIsInstance(checkpoints['x'], _UnboundDefinition)

        self.assertFalse(checkpoints['init'])
        self.assertIs(checkpoints['self'], None)

        self.assertIs(application, None)

    def test_main_default(self):
        self.assertEqual(main(), 0)

    def test_main_custom_application(self):
        stages = []
        instances = []

        class TestApplication(Application):
            def __init__(self):
                stages.append('init')
                instances.append(self)

            def parse_command_line(self, argv):
                stages.append('parse')
                instances.append(self)

            def run(self):
                stages.append('run')
                instances.append(self)
                return 0

        self.assertEqual(main(), 0)
        self.assertEqual(stages, ['init', 'parse', 'run'])
        self.assertGreater(len(instances), 0)
        application = instances[0]
        self.assertIsInstance(application, TestApplication)
        self.assertEqual(instances, len(stages)*[application])

    def test_main_custom_run(self):
        class TestApplication(Application):
            def run(self):
                return -1

        self.assertEqual(main(), -1)

    def test_main_custom_command_line(self):
        checkpoints = []

        class TestApplication(Application):
            def parse_command_line(self, argv):
                checkpoints.append(argv)

        self.assertEqual(main(), 0)
        self.assertEqual(len(checkpoints), 1)
        self.assertIsInstance(checkpoints[0], list)

    def test_main_custom_command_line_parsing_error(self):
        class TestError(Error):
            template = "Test Error"

        class TestApplication(Application):
            def parse_command_line(self, argv):
                raise TestError()

        sys.stderr = StringIO.StringIO()
        self.assertEqual(main(), 1)
        self.assertEqual(sys.stderr.getvalue(), '%s\n' % TestError.template)

test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestApplication)

if __name__ == '__main__':
    unittest.main()
