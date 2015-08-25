import inspect
import types

class _UnboundDefinition(object):
    def __init__(self, cls, arguments):
        self.cls = cls
        self.arguments = arguments

    def __call__(self, parent, identifier):
        args, kwargs = self.arguments
        args = (parent, identifier) + args
        return self.cls(*args, **kwargs)

def _extract(cls):
    return filter(lambda x: isinstance(x[1], _UnboundDefinition),
                  cls.__dict__.iteritems())

def _bind(instance, definitions):
    for identifier, value in definitions:
        setattr(instance, identifier, value(instance, identifier))

class _DefinitionMethaclass(type):
    def __call__(*args, **kwargs):
        from actuator.application import Application

        self = args[0]
        args = args[1:]
        if len(args) >= 2:
            parent, identifier = args[:2]
            if isinstance(parent, Application) and \
               isinstance(identifier, types.StringTypes):
                args = args[2:]
                definition = super(_DefinitionMethaclass, self). \
                                 __call__(*args, **kwargs)
                definition.bind(parent, identifier)
                return definition

        return _UnboundDefinition(self, (args, kwargs))

class Definition(object):
    __metaclass__ = _DefinitionMethaclass

    def bind(self, parent, identifier):
        self.parent = parent
        self.identifier = identifier
