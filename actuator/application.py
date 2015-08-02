class _Registry(object):
    def __init__(self):
        self.application = None

    def register(self, entity):
        if self.application is not None and self.application is not Application:
            raise Exception('Can\'t define %s as application class because ' \
                            '%s has already been defined' % \
                            (entity.__name__, self.application.__name__))

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
