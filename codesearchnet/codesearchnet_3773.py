def create(self, fail_on_found=False, force_on_exists=False, **kwargs):
        """Create a group.

        =====API DOCS=====
        Create a group.

        :param parent: Primary key or name of the group which will be the parent of created group.
        :type parent: str
        :param fail_on_found: Flag that if set, the operation fails if an object matching the unique criteria
                              already exists.
        :type fail_on_found: bool
        :param force_on_exists: Flag that if set, then if a match is found on unique fields, other fields will
                                be updated to the provided values.; If unset, a match causes the request to be
                                a no-op.
        :type force_on_exists: bool
        :param `**kwargs`: Keyword arguments which, all together, will be used as POST body to create the
                           resource object.
        :returns: A dictionary combining the JSON output of the created resource, as well as two extra fields:
                  "changed", a flag indicating if the resource is created successfully; "id", an integer which
                  is the primary key of the created object.
        :rtype: dict
        :raises tower_cli.exceptions.UsageError: When inventory is not provided in ``**kwargs`` and ``parent``
                                                 is not provided.

        =====API DOCS=====
        """
        if kwargs.get('parent', None):
            parent_data = self.set_child_endpoint(parent=kwargs['parent'], inventory=kwargs.get('inventory', None))
            kwargs['inventory'] = parent_data['inventory']
        elif 'inventory' not in kwargs:
            raise exc.UsageError('To create a group, you must provide a parent inventory or parent group.')
        return super(Resource, self).create(fail_on_found=fail_on_found, force_on_exists=force_on_exists, **kwargs)