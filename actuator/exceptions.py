import sherbet

class Error(Exception):
    def __init__(self, **kwargs):
        super(Error, self).__init__(sherbet.sweeten(self.template, **kwargs))

class ApplicationRedefined(Error):
    template = 'Class {other.__name__} can\'t be defined as application ' \
               'because {current.__name__} has already been defined.'

class InvalidDefinitionName(Error):
    template = 'Expected string as definition name but got {name} ' \
               'for definition {identifier} of {parent.__name__}.'

class InvalidSubstringInDefinitionName(Error):
    template = 'Name "{name}" of {parent.__name__} definition {identifier} ' \
               'shouldn\'t contain separator "{separator}".'

class DefinitionNamesAmbiguity(Error):
    template = 'Definition{identifiers_plural} {identifiers} of ' \
               '{parent.__name__} ha{identifiers_plural<ve|s>} the same name ' \
               '"{name}".'

class InvalidDefinitionArguments(Error):
    template = 'Definition {identifier} of {parent.__name__} raised error ' \
               '"{error}" on getting its arguments values.'

class UnrecognizedApplicationArgument(Error):
    template = 'Unrecognized option {name} for {application.__name__}.'

class InvalidDefinitionValue(Error):
    pass

class InvalidFlagValue(InvalidDefinitionValue):
    template = 'Can\'t treat "{value}" as vaild value for flag ' \
               '{identifier} of {parent.__name__}.'
