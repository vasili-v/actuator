import sherbet

class Error(Exception):
    def __init__(self, **kwargs):
        super(Error, self).__init__(sherbet.sweeten(self.template, **kwargs))

class ApplicationRedefined(Error):
    template = 'Class {other.__name__} can\'t be defined as application ' \
               'because {current.__name__} has already been defined.'
