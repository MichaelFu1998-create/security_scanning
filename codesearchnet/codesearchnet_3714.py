def get(self, pk=None, **kwargs):
        """Return one and exactly one object.

        Lookups may be through a primary key, specified as a positional argument, and/or through filters specified
        through keyword arguments.

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
        if kwargs.pop('include_debug_header', True):
            debug.log('Getting the record.', header='details')
        response = self.read(pk=pk, fail_on_no_results=True, fail_on_multiple_results=True, **kwargs)
        return response['results'][0]