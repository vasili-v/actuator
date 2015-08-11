import unittest

from actuator.exceptions import ApplicationRedefined
import actuator._registry as _registry
from actuator._registry import _get_application_class, _Registry
from actuator.application import Application

class Test_Registry(unittest.TestCase):
    def setUp(self):
        self.___get_application_class = _get_application_class

    def tearDown(self):
        _registry._get_application_class = self.___get_application_class

    def test__get_application_class(self):
        self.assertIs(_get_application_class(), Application)

    def test_registry(self):
        registry = _Registry()
        self.assertEqual(registry.application, None)

    def test_registry_register(self):
        class TestApplication(object):
            pass

        class RedefinedTestApplication(TestApplication):
            pass

        def initial_get_application_class():
            return None

        def further_get_application_class():
            return TestApplication

        _registry._get_application_class = initial_get_application_class

        registry = _Registry()

        registry.register(TestApplication)
        self.assertIs(registry.application, TestApplication)

        _registry._get_application_class = further_get_application_class

        registry.register(RedefinedTestApplication)
        self.assertIs(registry.application, RedefinedTestApplication)

    def test_registry_register_failure(self):
        class TestApplication(object):
            pass

        class RedefinedTestApplication(TestApplication):
            pass

        class OtherRedefinedTestApplication(TestApplication):
            pass

        def get_application_class():
            return TestApplication

        _registry._get_application_class = get_application_class

        registry = _Registry()
        registry.application = RedefinedTestApplication

        with self.assertRaises(ApplicationRedefined) as ctx:
            registry.register(OtherRedefinedTestApplication)

        self.assertIn('RedefinedTestApplication', str(ctx.exception))
        self.assertIn('OtherRedefinedTestApplication', str(ctx.exception))

test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(Test_Registry)

if __name__ == '__main__':
    unittest.main()
