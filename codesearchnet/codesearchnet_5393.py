def deserialize_workflow(self, s_state, workflow_spec=None,
                             read_only=False, **kwargs):
        """
        :param s_state: the state of the workflow as returned by
        serialize_workflow

        :param workflow_spec: the Workflow Spec of the workflow
        (CompactWorkflowSerializer only supports workflow serialization)

        :param read_only: (Optional) True if the workflow should be restored in
        READ ONLY mode

        NB: Additional kwargs passed to the deserialize_workflow method will be
        passed to the new_workflow method.
        """
        if workflow_spec is None:
            raise NotImplementedError(
                'Including the spec serialization with the workflow state is '
                ' not implemented. A \'workflow_spec\' must '
                'be provided.')
        workflow = self.new_workflow(
            workflow_spec, read_only=read_only, **kwargs)
        self._restore_workflow_state(workflow, s_state)
        return workflow