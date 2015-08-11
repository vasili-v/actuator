from actuator.exceptions import ApplicationRedefined

class _Registry(object):
    def __init__(self):
        self.application = None

    def register(self, entity):
        if self.application is not None and \
           self.application is not Application:
            raise ApplicationRedefined(other=entity, current=self.application)

        self.application = entity

_registry = _Registry()

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
