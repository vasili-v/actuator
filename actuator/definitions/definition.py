import inspect
import types

from actuator.exceptions import InvalidDefinitionName, \
                                InvalidSubstringInDefinitionName, \
                                DefinitionNamesAmbiguity, \
                                InvalidDefinitionArguments

class _Auto(object):
    pass

auto = _Auto()

class _Undefined(object):
    pass

Undefined = _Undefined()

class _AutoArgument(object):
    def __init__(self, identifier, specifications, values):
        self.identifier = identifier
        self.index = None
        self.required = False
        self.value = None

        try:
            self.index = specifications.args.index(self.identifier) - 1
        except ValueError:
            return

        self.required = identifier not in values or values[identifier] is auto
        if not self.required:
            self.value = values[identifier]

    @property
    def found(self):
        return self.index is not None

    def inject(self, args, kwargs):
        if self.found and self.required:
            if len(args) < self.index:
                kwargs[self.identifier] = self.value
            elif len(args) == self.index:
                if self.identifier in kwargs:
                    kwargs[self.identifier] = self.value
                else:
                    args += (self.value,)
            else:
                args = args[:self.index] + (self.value,) + args[self.index + 1:]

        return args

class _UnboundDefinition(object):
    def __init__(self, cls, arguments):
        self.cls = cls
        self.arguments = arguments

        specifications = inspect.getargspec(self.cls.__init__)
        args, kwargs = arguments
        args = (None,) + args
        try:
            values = inspect.getcallargs(self.cls.__init__, *args, **kwargs)
        except Exception as error:
            self.error = error
        else:
            self.error = None
            self.name = _AutoArgument('name', specifications, values)

    def __call__(self, parent, identifier):
        if self.error is not None:
            raise InvalidDefinitionArguments(error=self.error,
                                             parent=type(parent),
                                             identifier=identifier)

        args, kwargs = self.arguments
        args = (parent, identifier) + self.name.inject(args, kwargs)
        return self.cls(*args, **kwargs)

def _extract(cls):
    return filter(lambda x: isinstance(x[1], _UnboundDefinition),
                  cls.__dict__.iteritems())

def _make_name(indentifier):
    return indentifier.replace('_', '-')

def _validate_names(definition, names, instance):
    name = definition.name
    if name not in names:
        names[name] = []
    names[name].append(definition)

    if len(names[name]) > 1:
        identifiers = [definition.identifier for definition in names[name]]
        raise DefinitionNamesAmbiguity(identifiers=identifiers,
                                       parent=type(instance),
                                       name=name)

def _bind(instance, definitions):
    names = {}
    for indentifier, value in definitions:
        if value.error is None and value.name.found and value.name.required:
            value.name.value = _make_name(indentifier)

        definition = value(instance, indentifier)
        _validate_names(definition, names, instance)

        setattr(instance, indentifier, definition)

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
                definition.validate()
                return definition

        return _UnboundDefinition(self, (args, kwargs))

class Definition(object):
    __metaclass__ = _DefinitionMethaclass

    def __init__(self, name=auto, default=Undefined, nullable=False):
        self.name = name
        self.default = default
        self.nullable = nullable

    def validate(self):
        if not isinstance(self.name, types.StringTypes):
            raise InvalidDefinitionName(name=repr(self.name),
                                        identifier=self.identifier,
                                        parent=type(self.parent))

        from actuator._command_line_parser import _CommandLineParser
        separator = _CommandLineParser.actuator_argument_value_separator
        if separator in self.name:
            raise InvalidSubstringInDefinitionName(name=self.name,
                                                   identifier=self.identifier,
                                                   parent=type(self.parent),
                                                   separator=separator)

    def bind(self, parent, identifier):
        self.parent = parent
        self.identifier = identifier
