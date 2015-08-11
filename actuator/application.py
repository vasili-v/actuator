from actuator._registry import _registry

class _ApplicationMetaclass(type):
    def __init__(cls, name, bases, attributes):
        _registry.register(cls)

        super(_ApplicationMetaclass, cls).__init__(name, bases, attributes)

class Application(object):
    __metaclass__ = _ApplicationMetaclass

    def run(self):
        return 0

def main():
    return _registry.application().run()
