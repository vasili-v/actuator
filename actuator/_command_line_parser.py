import os

class _CommandLineScript(object):
    pass

command_line_script = _CommandLineScript()

class _CommandLineParser(object):
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
