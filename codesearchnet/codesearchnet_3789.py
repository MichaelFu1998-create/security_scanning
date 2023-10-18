def get(self, pk=None, **kwargs):
        """Return one and exactly one notification template.

        Note here configuration-related fields like
        'notification_configuration' and 'channels' will not be
        used even provided.

        Lookups may be through a primary key, specified as a positional
        argument, and/or through filters specified through keyword arguments.

        If the number of results does not equal one, raise an exception.

        =====API DOCS=====
        Retrieve one and exactly one object.

        :param pk: Primary key of the resource to be read. Tower CLI will only attempt to read *that* object
                   if ``pk`` is provided (not ``None``).
        :type pk: int
        :param `**kwargs`: Keyword arguments used to look up resource object to retrieve if ``pk`` is not provided.
        :returns: loaded JSON of the retrieved resource object.
        :rtype: dict

        =====API DOCS=====
        """
        self._separate(kwargs)
        return super(Resource, self).get(pk=pk, **kwargs)