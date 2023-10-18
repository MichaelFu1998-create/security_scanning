def new_workflow(self, workflow_spec, read_only=False, **kwargs):
        """
        Create a new workflow instance from the given spec and arguments.

        :param workflow_spec: the workflow spec to use

        :param read_only: this should be in read only mode

        :param kwargs: Any extra kwargs passed to the deserialize_workflow
        method will be passed through here
        """
        return BpmnWorkflow(workflow_spec, read_only=read_only, **kwargs)