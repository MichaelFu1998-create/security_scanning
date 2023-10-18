def launch(self, workflow_job_template=None, monitor=False, wait=False,
               timeout=None, extra_vars=None, **kwargs):
        """Launch a new workflow job based on a workflow job template.

        Creates a new workflow job in Ansible Tower, starts it, and
        returns back an ID in order for its status to be monitored.

        =====API DOCS=====
        Launch a new workflow job based on a workflow job template.

        :param workflow_job_template: Primary key or name of the workflow job template to launch new job.
        :type workflow_job_template: str
        :param monitor: Flag that if set, immediately calls ``monitor`` on the newly launched workflow job rather
                        than exiting with a success.
        :type monitor: bool
        :param wait: Flag that if set, monitor the status of the workflow job, but do not print while job is
                     in progress.
        :type wait: bool
        :param timeout: If provided with ``monitor`` flag set, this attempt will time out after the given number
                        of seconds.
        :type timeout: int
        :param extra_vars: yaml formatted texts that contains extra variables to pass on.
        :type extra_vars: array of strings
        :param `**kwargs`: Fields needed to create and launch a workflow job.
        :returns: Result of subsequent ``monitor`` call if ``monitor`` flag is on; Result of subsequent ``wait``
                  call if ``wait`` flag is on; loaded JSON output of the job launch if none of the two flags are on.
        :rtype: dict

        =====API DOCS=====
        """
        if extra_vars is not None and len(extra_vars) > 0:
            kwargs['extra_vars'] = parser.process_extra_vars(extra_vars)

        debug.log('Launching the workflow job.', header='details')
        self._pop_none(kwargs)
        post_response = client.post('workflow_job_templates/{0}/launch/'.format(
            workflow_job_template), data=kwargs).json()

        workflow_job_id = post_response['id']
        post_response['changed'] = True

        if monitor:
            return self.monitor(workflow_job_id, timeout=timeout)
        elif wait:
            return self.wait(workflow_job_id, timeout=timeout)

        return post_response