def stderr(self):
        '''Get stderr from all the tasks of a workflow.

        Returns:
            (list): tasks with their stderr

        Example:
            >>> workflow.stderr
            [
                {
                    "id": "4488895771403082552",
                    "taskType": "AOP_Strip_Processor",
                    "name": "Task1",
                    "stderr": "............"
                }
            ]

        '''

        if not self.id:
            raise WorkflowError('Workflow is not running.  Cannot get stderr.')
        if self.batch_values:
            raise NotImplementedError("Query Each Workflow Id within the Batch Workflow for stderr.")

        wf = self.workflow.get(self.id)

        stderr_list = []
        for task in wf['tasks']:
            stderr_list.append(
                {
                    'id': task['id'],
                    'taskType': task['taskType'],
                    'name': task['name'],
                    'stderr': self.workflow.get_stderr(self.id, task['id'])
                }
            )

        return stderr_list