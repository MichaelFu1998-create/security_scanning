def list_all(cls, basic = None):
        """List known settings.

        :Parameters:
            - `basic`: When `True` then limit output to the basic settings,
              when `False` list only the extra settings.
        """
        if basic is None:
            return [s for s in cls._defs]
        else:
            return [s.name for s in cls._defs.values() if s.basic == basic]