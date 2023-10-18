def modify(self, pk=None, create_on_missing=False, **kwargs):
        """Modify an existing notification template.

        Not all required configuration-related fields (required according to
        notification_type) should be provided.

        Fields in the resource's `identity` tuple can be used in lieu of a
        primary key for a lookup; in such a case, only other fields are
        written.

        To modify unique fields, you must use the primary key for the lookup.

        =====API DOCS=====
        Modify an already existing object.

        :param pk: Primary key of the resource to be modified.
        :type pk: int
        :param create_on_missing: Flag that if set, a new object is created if ``pk`` is not set and objects
                                  matching the appropriate unique criteria is not found.
        :type create_on_missing: bool
        :param `**kwargs`: Keyword arguments which, all together, will be used as PATCH body to modify the
                           resource object. if ``pk`` is not set, key-value pairs of ``**kwargs`` which are
                           also in resource's identity will be used to lookup existing reosource.
        :returns: A dictionary combining the JSON output of the modified resource, as well as two extra fields:
                  "changed", a flag indicating if the resource is successfully updated; "id", an integer which
                  is the primary key of the updated object.
        :rtype: dict

        =====API DOCS=====
        """
        # Create the resource if needed.
        if pk is None and create_on_missing:
            try:
                self.get(**copy.deepcopy(kwargs))
            except exc.NotFound:
                return self.create(**kwargs)

        # Modify everything except notification type and configuration
        config_item = self._separate(kwargs)
        notification_type = kwargs.pop('notification_type', None)
        debug.log('Modify everything except notification type and'
                  ' configuration', header='details')
        part_result = super(Resource, self).\
            modify(pk=pk, create_on_missing=create_on_missing, **kwargs)

        # Modify notification type and configuration
        if notification_type is None or \
           notification_type == part_result['notification_type']:
            for item in part_result['notification_configuration']:
                if item not in config_item or not config_item[item]:
                    to_add = part_result['notification_configuration'][item]
                    if not (to_add == '$encrypted$' and
                            item in Resource.encrypted_fields):
                        config_item[item] = to_add
        if notification_type is None:
            kwargs['notification_type'] = part_result['notification_type']
        else:
            kwargs['notification_type'] = notification_type
        self._configuration(kwargs, config_item)
        debug.log('Modify notification type and configuration',
                  header='details')
        result = super(Resource, self).\
            modify(pk=pk, create_on_missing=create_on_missing, **kwargs)

        # Update 'changed' field to give general changed info
        if 'changed' in result and 'changed' in part_result:
            result['changed'] = result['changed'] or part_result['changed']
        return result