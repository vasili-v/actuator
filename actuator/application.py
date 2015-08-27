import sys

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

class Application(object):
    __metaclass__ = _ApplicationMetaclass

    def process_command_line(self, argv):
        pass

    def run(self):
        return 0

def main():
    application = _registry.application()
    try:
        application.process_command_line(sys.argv)
    except Error as error:
        print >> sys.stderr, error
        return 1

    return _registry.application().run()
