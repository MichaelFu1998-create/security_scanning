def all(self, workflow_id):
        """
        Get information about subscribers who were removed from an Automation
        workflow.

        :param workflow_id: The unique id for the Automation workflow.
        :type workflow_id: :py:class:`str`
        """
        self.workflow_id = workflow_id
        return self._mc_client._get(url=self._build_path(workflow_id, 'removed-subscribers'))