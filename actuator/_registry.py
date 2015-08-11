from actuator.exceptions import ApplicationRedefined

def _get_application_class():
    try:
        import actuator.application as application
        return application.Application
    except AttributeError:
        return None

class _Registry(object):
    def __init__(self):
        self.application = None

    def register(self, entity):
        if self.application is not _get_application_class():
            raise ApplicationRedefined(other=entity, current=self.application)

        self.application = entity

_registry = _Registry()
