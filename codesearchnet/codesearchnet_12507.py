def task_ids(self):
        '''
        Get the task IDs of a running workflow

        Args:
            None

        Returns:
            List of task IDs
        '''
        if not self.id:
            raise WorkflowError('Workflow is not running.  Cannot get task IDs.')

        if self.batch_values:
            raise NotImplementedError("Query Each Workflow Id within the Batch Workflow for task IDs.")

        wf = self.workflow.get(self.id)

        return [task['id'] for task in wf['tasks']]