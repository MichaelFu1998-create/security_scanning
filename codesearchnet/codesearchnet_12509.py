def stdout(self):
        ''' Get stdout from all the tasks of a workflow.

        Returns:
            (list): tasks with their stdout
        
        Example:
            >>> workflow.stdout
            [
                {
                    "id": "4488895771403082552",
                    "taskType": "AOP_Strip_Processor",
                    "name": "Task1",
                    "stdout": "............"
                }
            ]

        '''
        if not self.id:
            raise WorkflowError('Workflow is not running.  Cannot get stdout.')
        if self.batch_values:
            raise NotImplementedError("Query Each Workflow Id within the Batch Workflow for stdout.")

        wf = self.workflow.get(self.id)

        stdout_list = []
        for task in wf['tasks']:
            stdout_list.append(
                {
                    'id': task['id'],
                    'taskType': task['taskType'],
                    'name': task['name'],
                    'stdout': self.workflow.get_stdout(self.id, task['id'])
                }
            )

        return stdout_list