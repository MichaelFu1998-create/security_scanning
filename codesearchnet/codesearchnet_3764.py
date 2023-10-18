def get(self, pk=None, **kwargs):
        """Get information about a role.

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
            debug.log('Getting the role record.', header='details')
        data, self.endpoint = self.data_endpoint(kwargs)
        response = self.read(pk=pk, fail_on_no_results=True,
                             fail_on_multiple_results=True, **data)
        item_dict = response['results'][0]
        self.configure_display(item_dict)
        return item_dict