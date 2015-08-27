import sys
import os

from actuator.exceptions import Error
from actuator._utils import _initialize_class
from actuator._registry import _registry
from actuator.definitions.definition import _extract, _bind

class _ApplicationMetaclass(type):
    def __init__(cls, name, bases, attributes):
        _registry.register(cls)

        super(_ApplicationMetaclass, cls).__init__(name, bases, attributes)

    def __call__(*args, **kwargs):
        cls = args[0]
        definitions = _extract(cls)

        application = cls.__new__(*args, **kwargs)
        if application is not None:
            _bind(application, definitions)
            _initialize_class(application, args[1:], kwargs)

        return application

class _CommandLineScript(object):
    pass

command_line_script = _CommandLineScript()

class Application(object):
    __metaclass__ = _ApplicationMetaclass

    actuator_executable = None
    actuator_executable_directory = None
    actuator_executable_name = None

    def parse_executable_path(self, path):
        if os.path.isfile(path):
            self.actuator_executable = path
            directory, name = os.path.split(path)
            if directory and os.path.isdir(directory):
                self.actuator_executable_directory = directory
            if name:
                self.actuator_executable_name = name

        elif path == '-c':
            self.actuator_executable = command_line_script

    def parse_command_line(self, argv):
        if argv:
            self.parse_executable_path(argv[0])

    def run(self):
        return 0

def main():
    application = _registry.application()
    try:
        application.parse_command_line(sys.argv)
    except Error as error:
        print >> sys.stderr, error
        return 1

    return application.run()
