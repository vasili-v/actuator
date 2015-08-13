def _initialize_class(cls, args, kwargs):
    result = cls.__init__(*args, **kwargs)
    if result is not None:
        raise TypeError('__init__() should return None, not \'%s\'' % \
                        type(result).__name__)
