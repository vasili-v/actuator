import os

from actuator.exceptions import UnrecognizedApplicationArgument
from actuator.definitions.definition import Definition

class _CommandLineScript(object):
    pass

command_line_script = _CommandLineScript()

class _CommandLineParser(object):
    actuator_executable = None
    actuator_executable_directory = None
    actuator_executable_name = None

    actuator_argument_name_prefix = '--'
    actuator_argument_value_separator = '='

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

    def __make_definition_names_index(self):
        for identifier in dir(self):
            attribute = getattr(self, identifier)
            if isinstance(attribute, Definition):
                yield attribute.name, attribute

    def __split_argument_name_and_value(self, argument):
        position = argument.find(self.actuator_argument_value_separator)
        if position >= 0:
            return argument[:position], argument[position + 1:]

        return argument, None

    def parse_named_argument(self, argument, names):
        name, value = self.__split_argument_name_and_value(argument)

        try:
            definition = names[name]
        except KeyError:
            raise UnrecognizedApplicationArgument(name=name,
                                                  application=type(self))

        setattr(self, definition.identifier, definition.parse(value))

    def parse_command_line_arguments(self, arguments):
        names = dict(self.__make_definition_names_index())

        name_prefix_length = len(self.actuator_argument_name_prefix)
        for argument in arguments:
            if argument.startswith(self.actuator_argument_name_prefix):
                self.parse_named_argument(argument[name_prefix_length:], names)
            else:
                raise UnrecognizedApplicationArgument(name=argument,
                                                      application=type(self))

    def parse_command_line(self, argv):
        if argv:
            self.parse_executable_path(argv[0])
            self.parse_command_line_arguments(argv[1:])
