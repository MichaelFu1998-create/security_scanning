def write(self, pk=None, create_on_missing=False, fail_on_found=False, force_on_exists=True, **kwargs):
        """
        =====API DOCS=====
        Modify the given object using the Ansible Tower API.

        :param pk: Primary key of the resource to be read. Tower CLI will only attempt to read that object
                   if ``pk`` is provided (not ``None``).
        :type pk: int
        :param create_on_missing: Flag that if set, a new object is created if ``pk`` is not set and objects
                                  matching the appropriate unique criteria is not found.
        :type create_on_missing: bool
        :param fail_on_found: Flag that if set, the operation fails if an object matching the unique criteria
                              already exists.
        :type fail_on_found: bool
        :param force_on_exists: Flag that if set, then if an object is modified based on matching via unique
                                fields (as opposed to the primary key), other fields are updated based on data
                                sent; If unset, then the non-unique values are only written in a creation case.
        :type force_on_exists: bool
        :param `**kwargs`: Keyword arguments which, all together, will be used as POST/PATCH body to create/modify
                           the resource object. if ``pk`` is not set, key-value pairs of ``**kwargs`` which are
                           also in resource's identity will be used to lookup existing reosource.
        :returns: A dictionary combining the JSON output of the resource, as well as two extra fields: "changed",
                  a flag indicating if the resource is created or successfully updated; "id", an integer which
                  is the primary key of the specified object.
        :rtype: dict
        :raises tower_cli.exceptions.BadRequest: When required fields are missing in ``**kwargs`` when creating
                                                 a new resource object.

        =====API DOCS=====
        """
        existing_data = {}

        # Remove default values (anything where the value is None).
        self._pop_none(kwargs)

        # Determine which record we are writing, if we weren't given a primary key.
        if not pk:
            debug.log('Checking for an existing record.', header='details')
            existing_data = self._lookup(
                fail_on_found=fail_on_found, fail_on_missing=not create_on_missing, include_debug_header=False,
                **kwargs
            )
            if existing_data:
                pk = existing_data['id']
        else:
            # We already know the primary key, but get the existing data.
            # This allows us to know whether the write made any changes.
            debug.log('Getting existing record.', header='details')
            existing_data = self.get(pk)

        # Sanity check: Are we missing required values?
        # If we don't have a primary key, then all required values must be set, and if they're not, it's an error.
        missing_fields = []
        for i in self.fields:
            if i.key not in kwargs and i.name not in kwargs and i.required:
                missing_fields.append(i.key or i.name)
        if missing_fields and not pk:
            raise exc.BadRequest('Missing required fields: %s' % ', '.join(missing_fields).replace('_', '-'))

        # Sanity check: Do we need to do a write at all?
        # If `force_on_exists` is False and the record was, in fact, found, then no action is required.
        if pk and not force_on_exists:
            debug.log('Record already exists, and --force-on-exists is off; do nothing.', header='decision', nl=2)
            answer = OrderedDict((('changed', False), ('id', pk)))
            answer.update(existing_data)
            return answer

        # Similarly, if all existing data matches our write parameters, there's no need to do anything.
        if all([kwargs[k] == existing_data.get(k, None) for k in kwargs.keys()]):
            debug.log('All provided fields match existing data; do nothing.', header='decision', nl=2)
            answer = OrderedDict((('changed', False), ('id', pk)))
            answer.update(existing_data)
            return answer

        # Reinsert None for special case of null association
        for key in kwargs:
            if kwargs[key] == 'null':
                kwargs[key] = None

        # Get the URL and method to use for the write.
        url = self.endpoint
        method = 'POST'
        if pk:
            url = self._get_patch_url(url, pk)
            method = 'PATCH'

        # If debugging is on, print the URL and data being sent.
        debug.log('Writing the record.', header='details')

        # Actually perform the write.
        r = getattr(client, method.lower())(url, data=kwargs)

        # At this point, we know the write succeeded, and we know that data was changed in the process.
        answer = OrderedDict((('changed', True), ('id', r.json()['id'])))
        answer.update(r.json())
        return answer