def create(self, organization=None, monitor=False, wait=False,
               timeout=None, fail_on_found=False, force_on_exists=False,
               **kwargs):
        """Create a new item of resource, with or w/o org.
        This would be a shared class with user, but it needs the ability
        to monitor if the flag is set.

        =====API DOCS=====
        Create a project and, if related flags are set, monitor or wait the triggered initial project update.

        :param monitor: Flag that if set, immediately calls ``monitor`` on the newly triggered project update
                        rather than exiting with a success.
        :type monitor: bool
        :param wait: Flag that if set, monitor the status of the triggered project update, but do not print
                     while it is in progress.
        :type wait: bool
        :param timeout: If provided with ``monitor`` flag set, this attempt will time out after the given number
                        of seconds.
        :type timeout: bool
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
        if 'job_timeout' in kwargs and 'timeout' not in kwargs:
            kwargs['timeout'] = kwargs.pop('job_timeout')

        post_associate = False
        if organization:
            # Processing the organization flag depends on version
            debug.log('Checking Organization Relationship.', header='details')
            r = client.options('/projects/')
            if 'organization' in r.json().get('actions', {}).get('POST', {}):
                kwargs['organization'] = organization
            else:
                post_associate = True

        # First, run the create method, ignoring the organization given
        answer = super(Resource, self).write(
            create_on_missing=True,
            fail_on_found=fail_on_found, force_on_exists=force_on_exists,
            **kwargs
        )
        project_id = answer['id']

        # If an organization is given, associate it here
        if post_associate:

            # Get the organization from Tower, will lookup name if needed
            org_resource = get_resource('organization')
            org_data = org_resource.get(organization)
            org_pk = org_data['id']

            debug.log("associating the project with its organization",
                      header='details', nl=1)
            org_resource._assoc('projects', org_pk, project_id)

        # if the monitor flag is set, wait for the SCM to update
        if monitor and answer.get('changed', False):
            return self.monitor(pk=None, parent_pk=project_id, timeout=timeout)
        elif wait and answer.get('changed', False):
            return self.wait(pk=None, parent_pk=project_id, timeout=timeout)

        return answer