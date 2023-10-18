def validate(method):
    """
    Config option name value validator decorator.
    """
    # Name error template
    name_error = 'configuration option "{}" is not supported'

    @functools.wraps(method)
    def validator(self, name, *args):
        if name not in self.allowed_opts:
            raise ValueError(name_error.format(name))
        return method(self, name, *args)
    return validator