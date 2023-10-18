def launch(self, job_template=None, monitor=False, wait=False,
               timeout=None, no_input=True, extra_vars=None, **kwargs):
        """Launch a new job based on a job template.

        Creates a new job in Ansible Tower, immediately starts it, and
        returns back an ID in order for its status to be monitored.

        =====API DOCS=====
        Launch a new job based on a job template.

        :param job_template: Primary key or name of the job template to launch new job.
        :type job_template: str
        :param monitor: Flag that if set, immediately calls ``monitor`` on the newly launched job rather
                        than exiting with a success.
        :type monitor: bool
        :param wait: Flag that if set, monitor the status of the job, but do not print while job is in progress.
        :type wait: bool
        :param timeout: If provided with ``monitor`` flag set, this attempt will time out after the given number
                        of seconds.
        :type timeout: int
        :param no_input: Flag that if set, suppress any requests for input.
        :type no_input: bool
        :param extra_vars: yaml formatted texts that contains extra variables to pass on.
        :type extra_vars: array of strings
        :param diff_mode: Specify diff mode for job template to run.
        :type diff_mode: bool
        :param limit: Specify host limit for job template to run.
        :type limit: str
        :param tags: Specify tagged actions in the playbook to run.
        :type tags: str
        :param skip_tags: Specify tagged actions in the playbook to omit.
        :type skip_tags: str
        :param job_type: Specify job type for job template to run.
        :type job_type: str
        :param verbosity: Specify verbosity of the playbook run.
        :type verbosity: int
        :param inventory: Specify machine credential for job template to run.
        :type inventory: str
        :param credential: Specify machine credential for job template to run.
        :type credential: str
        :returns: Result of subsequent ``monitor`` call if ``monitor`` flag is on; Result of subsequent
                  ``wait`` call if ``wait`` flag is on; Result of subsequent ``status`` call if none of
                  the two flags are on.
        :rtype: dict

        =====API DOCS=====
        """
        # Get the job template from Ansible Tower.
        # This is used as the baseline for starting the job.

        tags = kwargs.get('tags', None)
        jt_resource = get_resource('job_template')
        jt = jt_resource.get(job_template)

        # Update the job data by adding an automatically-generated job name,
        # and removing the ID.
        data = {}
        if tags:
            data['job_tags'] = tags

        # Initialize an extra_vars list that starts with the job template
        # preferences first, if they exist
        extra_vars_list = []
        if 'extra_vars' in data and len(data['extra_vars']) > 0:
            # But only do this for versions before 2.3
            debug.log('Getting version of Tower.', header='details')
            r = client.get('/config/')
            if LooseVersion(r.json()['version']) < LooseVersion('2.4'):
                extra_vars_list = [data['extra_vars']]

        # Add the runtime extra_vars to this list
        if extra_vars:
            extra_vars_list += list(extra_vars)  # accept tuples

        # If the job template requires prompting for extra variables,
        # do so (unless --no-input is set).
        if jt.get('ask_variables_on_launch', False) and not no_input \
                and not extra_vars:
            # If JT extra_vars are JSON, echo them to user as YAML
            initial = parser.process_extra_vars(
                [jt['extra_vars']], force_json=False
            )
            initial = '\n'.join((
                '# Specify extra variables (if any) here as YAML.',
                '# Lines beginning with "#" denote comments.',
                initial,
            ))
            extra_vars = click.edit(initial) or ''
            if extra_vars != initial:
                extra_vars_list = [extra_vars]

        # Data is starting out with JT variables, and we only want to
        # include extra_vars that come from the algorithm here.
        data.pop('extra_vars', None)

        # Replace/populate data fields if prompted.
        modified = set()
        for resource in PROMPT_LIST:
            if jt.pop('ask_' + resource + '_on_launch', False) and not no_input:
                resource_object = kwargs.get(resource, None)
                if type(resource_object) == types.Related:
                    resource_class = get_resource(resource)
                    resource_object = resource_class.get(resource).pop('id', None)
                if resource_object is None:
                    debug.log('{0} is asked at launch but not provided'.
                              format(resource), header='warning')
                elif resource != 'tags':
                    data[resource] = resource_object
                    modified.add(resource)

        # Dump extra_vars into JSON string for launching job
        if len(extra_vars_list) > 0:
            data['extra_vars'] = parser.process_extra_vars(
                extra_vars_list, force_json=True
            )

        # Create the new job in Ansible Tower.
        start_data = {}
        endpoint = '/job_templates/%d/launch/' % jt['id']
        if 'extra_vars' in data and len(data['extra_vars']) > 0:
            start_data['extra_vars'] = data['extra_vars']
        if tags:
            start_data['job_tags'] = data['job_tags']
        for resource in PROMPT_LIST:
            if resource in modified:
                start_data[resource] = data[resource]

        # There's a non-trivial chance that we are going to need some
        # additional information to start the job; in particular, many jobs
        # rely on passwords entered at run-time.
        #
        # If there are any such passwords on this job, ask for them now.
        debug.log('Asking for information necessary to start the job.',
                  header='details')
        job_start_info = client.get(endpoint).json()
        for password in job_start_info.get('passwords_needed_to_start', []):
            start_data[password] = getpass('Password for %s: ' % password)

        # Actually start the job.
        debug.log('Launching the job.', header='details')
        self._pop_none(kwargs)
        kwargs.update(start_data)
        job_started = client.post(endpoint, data=kwargs)

        # Get the job ID from the result.
        job_id = job_started.json()['id']

        # If returning json indicates any ignored fields, display it in
        # verbose mode.
        if job_started.text == '':
            ignored_fields = {}
        else:
            ignored_fields = job_started.json().get('ignored_fields', {})
        has_ignored_fields = False
        for key, value in ignored_fields.items():
            if value and value != '{}':
                if not has_ignored_fields:
                    debug.log('List of ignored fields on the server side:',
                              header='detail')
                    has_ignored_fields = True
                debug.log('{0}: {1}'.format(key, value))

        # Get some information about the running job to print
        result = self.status(pk=job_id, detail=True)
        result['changed'] = True

        # If we were told to monitor the job once it started, then call
        # monitor from here.
        if monitor:
            return self.monitor(job_id, timeout=timeout)
        elif wait:
            return self.wait(job_id, timeout=timeout)

        return result