def pause(self, workflow_id, email_id):
        """
        Pause an automated email.

        :param workflow_id: The unique id for the Automation workflow.
        :type workflow_id: :py:class:`str`
        :param email_id: The unique id for the Automation workflow email.
        :type email_id: :py:class:`str`
        """
        self.workflow_id = workflow_id
        self.email_id = email_id
        return self._mc_client._post(url=self._build_path(workflow_id, 'emails', email_id, 'actions/pause'))