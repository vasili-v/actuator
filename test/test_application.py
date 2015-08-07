import unittest

from actuator.application import _registry, Application, main

class TestApplication(unittest.TestCase):
    def tearDown(self):
        _registry.application = Application

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

        with self.assertRaises(Exception) as ctx:
            class SecondTestApplication(Application):
                pass

    def test_main_default(self):
        self.assertEqual(main(), 0)

    def test_main_custom(self):
        class TestApplication(Application):
            def run(self):
                return -1

        self.assertEqual(main(), -1)

test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestApplication)

if __name__ == '__main__':
    unittest.main()
