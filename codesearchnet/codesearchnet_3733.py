def create(self, fail_on_found=False, force_on_exists=False, **kwargs):
        """Create a new label.

        There are two types of label creation: isolatedly creating a new label and creating a new label under
        a job template. Here the two types are discriminated by whether to provide --job-template option.

        Fields in the resource's `identity` tuple are used for a lookup; if a match is found, then no-op (unless
        `force_on_exists` is set) but do not fail (unless `fail_on_found` is set).

        =====API DOCS=====
        Create a label.

        :param job_template: Primary key or name of the job template for the created label to associate to.
        :type job_template: str
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
        :raises tower_cli.exceptions.TowerCLIError: When the label already exists and ``fail_on_found`` flag is on.

        =====API DOCS=====
        """
        jt_id = kwargs.pop('job_template', None)
        old_endpoint = self.endpoint
        if jt_id is not None:
            jt = get_resource('job_template')
            jt.get(pk=jt_id)
            try:
                label_id = self.get(name=kwargs.get('name', None), organization=kwargs.get('organization', None))['id']
            except exc.NotFound:
                pass
            else:
                if fail_on_found:
                    raise exc.TowerCLIError('Label already exists and fail-on-found is switched on. Please use'
                                            ' "associate_label" method of job_template instead.')
                else:
                    debug.log('Label already exists, associating with job template.', header='details')
                    return jt.associate_label(job_template=jt_id, label=label_id)
            self.endpoint = '/job_templates/%d/labels/' % jt_id
        result = super(Resource, self).create(fail_on_found=fail_on_found, force_on_exists=force_on_exists, **kwargs)
        self.endpoint = old_endpoint
        return result