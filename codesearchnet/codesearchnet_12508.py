def cancel(self):
        '''
        Cancel a running workflow.

        Args:
            None

        Returns:
            None
        '''
        if not self.id:
            raise WorkflowError('Workflow is not running.  Cannot cancel.')

        if self.batch_values:
            self.workflow.batch_workflow_cancel(self.id)
        else:
            self.workflow.cancel(self.id)