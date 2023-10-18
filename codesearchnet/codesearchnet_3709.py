def _lookup(self, fail_on_missing=False, fail_on_found=False, include_debug_header=True, **kwargs):
        """
        =====API DOCS=====
        Attempt to perform a lookup that is expected to return a single result, and return the record.

        This method is a wrapper around `get` that strips out non-unique keys, and is used internally by
        `write` and `delete`.

        :param fail_on_missing: Flag that raise exception if no resource is found.
        :type fail_on_missing: bool
        :param fail_on_found: Flag that raise exception if a resource is found.
        :type fail_on_found: bool
        :param include_debug_header: Flag determining whether to print debug messages when querying
                                     Tower backend.
        :type include_debug_header: bool
        :param `**kwargs`: Keyword arguments list of available fields used for searching resource.
        :returns: A JSON object containing details of the resource returned by Tower backend.
        :rtype: dict

        :raises tower_cli.exceptions.BadRequest: When no field are provided in kwargs.
        :raises tower_cli.exceptions.Found: When a resource is found and fail_on_found flag is on.
        :raises tower_cli.exceptions.NotFound: When no resource is found and fail_on_missing flag
                                               is on.
        =====API DOCS=====
        """
        read_params = {}
        for field_name in self.identity:
            if field_name in kwargs:
                read_params[field_name] = kwargs[field_name]
        if 'id' in self.identity and len(self.identity) == 1:
            return {}
        if not read_params:
            raise exc.BadRequest('Cannot reliably determine which record to write. Include an ID or unique '
                                 'fields.')
        try:
            existing_data = self.get(include_debug_header=include_debug_header, **read_params)
            if fail_on_found:
                raise exc.Found('A record matching %s already exists, and you requested a failure in that case.' %
                                read_params)
            return existing_data
        except exc.NotFound:
            if fail_on_missing:
                raise exc.NotFound('A record matching %s does not exist, and you requested a failure in that case.' %
                                   read_params)
            return {}