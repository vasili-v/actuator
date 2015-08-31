import types
import json

from actuator.exceptions import InvalidFlagValue
from actuator.definitions.definition import auto, Definition

_NONE_VALUES = ('none', 'null', 'nil')

_FLAG_VALUES = {'true': True, 'false': False,
                'yes': True, 'no': False,
                'on': True, 'off': False}

class Flag(Definition):
    def __init__(self, name=auto, presence=True, default=False, nullable=False):
        super(Flag, self).__init__(name, default, nullable)
        self.presence = presence

    def parse(self, value):
        if not isinstance(value, types.StringTypes):
            return self.presence

        try:
            converted = json.loads(value)
        except Exception:
            converted = value
        else:
            if converted is None and self.nullable:
                return None

            if isinstance(converted, (int, long, float)):
                return converted != 0

            if not isinstance(converted, types.StringTypes):
                converted = value

        try:
            number = float(converted.strip())
        except Exception:
            pass
        else:
            return number != 0

        if value in _NONE_VALUES and self.nullable:
            return None

        try:
            return _FLAG_VALUES[converted.lower()]
        except KeyError:
            raise InvalidFlagValue(value=value,
                                   identifier=self.identifier,
                                   parent=type(self.parent))
