def configure_custom(self, config):
        """Configure an object with a user-supplied factory."""
        c = config.pop('()')
        if not hasattr(c, '__call__') and \
                hasattr(types, 'ClassType') and isinstance(c, types.ClassType):
            c = self.resolve(c)
        props = config.pop('.', None)
        # Check for valid identifiers
        kwargs = dict((k, config[k]) for k in config if valid_ident(k))
        result = c(**kwargs)
        if props:
            for name, value in props.items():
                setattr(result, name, value)
        return result