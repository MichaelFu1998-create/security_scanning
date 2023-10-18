def get(self, workflow_id, **queryparams):
        """
        Get a summary of an individual Automation workflow’s settings and
        content. The trigger_settings object returns information for the first
        email in the workflow.

        :param workflow_id: The unique id for the Automation workflow
        :type workflow_id: :py:class:`str`
        :param queryparams: the query string parameters
        queryparams['fields'] = []
        queryparams['exclude_fields'] = []
        """
        self.workflow_id = workflow_id
        return self._mc_client._get(url=self._build_path(workflow_id), **queryparams)