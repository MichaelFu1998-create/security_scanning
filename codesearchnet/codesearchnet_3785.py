def create(self, fail_on_found=False, force_on_exists=False, **kwargs):
        """Create a notification template.

        All required configuration-related fields (required according to
        notification_type) must be provided.

        There are two types of notification template creation: isolatedly
        creating a new notification template and creating a new notification
        template under a job template. Here the two types are discriminated by
        whether to provide --job-template option. --status option controls
        more specific, job-run-status-related association.

        Fields in the resource's `identity` tuple are used for a lookup;
        if a match is found, then no-op (unless `force_on_exists` is set) but
        do not fail (unless `fail_on_found` is set).

        =====API DOCS=====
        Create an object.

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

        =====API DOCS=====
        """
        config_item = self._separate(kwargs)
        jt_id = kwargs.pop('job_template', None)
        status = kwargs.pop('status', 'any')
        old_endpoint = self.endpoint
        if jt_id is not None:
            jt = get_resource('job_template')
            jt.get(pk=jt_id)
            try:
                nt_id = self.get(**copy.deepcopy(kwargs))['id']
            except exc.NotFound:
                pass
            else:
                if fail_on_found:
                    raise exc.TowerCLIError('Notification template already '
                                            'exists and fail-on-found is '
                                            'switched on. Please use'
                                            ' "associate_notification" method'
                                            ' of job_template instead.')
                else:
                    debug.log('Notification template already exists, '
                              'associating with job template.',
                              header='details')
                    return jt.associate_notification_template(
                        jt_id, nt_id, status=status)
            self.endpoint = '/job_templates/%d/notification_templates_%s/' %\
                            (jt_id, status)
        self._configuration(kwargs, config_item)
        result = super(Resource, self).create(**kwargs)
        self.endpoint = old_endpoint
        return result