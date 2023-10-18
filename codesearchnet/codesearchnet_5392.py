def serialize_workflow(self, workflow, include_spec=False, **kwargs):
        """
        :param workflow: the workflow instance to serialize

        :param include_spec: Always set to False (The CompactWorkflowSerializer
        only supports workflow serialization)
        """
        if include_spec:
            raise NotImplementedError(
                'Including the spec serialization with the workflow state '
                'is not implemented.')
        return self._get_workflow_state(workflow)