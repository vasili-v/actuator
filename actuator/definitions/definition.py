class _UnboundDefinition(object):
    def __init__(self, cls, arguments):
        self.cls = cls
        self.arguments = arguments

    def __call__(self, parent):
        args, kwargs = self.arguments
        args += (parent,) + args
        return self.cls(*args, **kwargs)

def _extract(cls):
    return filter(lambda x: isinstance(x[1], _UnboundDefinition),
                  cls.__dict__.iteritems())

def _bind(instance, definitions):
    for name, value in definitions:
        setattr(instance, name, value(instance))

class _DefinitionMethaclass(type):
    def __call__(*args, **kwargs):
        from actuator.application import Application

        self = args[0]
        args = args[1:]
        if len(args) > 0 and isinstance(args[0], Application):
            parent = args[0]
            args = args[1:]
            definition = super(_DefinitionMethaclass, self). \
                             __call__(*args, **kwargs)
            definition.bind(parent)
            return definition

        return _UnboundDefinition(self, (args, kwargs))

class Definition(object):
    __metaclass__ = _DefinitionMethaclass

    def bind(self, parent):
        self.parent = parent
