def execute(self):
        '''
        Execute the workflow.

        Args:
            None

        Returns:
            Workflow_id
        '''
        # if not self.tasks:
        #     raise WorkflowError('Workflow contains no tasks, and cannot be executed.')

        # for task in self.tasks:
        #     self.definition['tasks'].append( task.generate_task_workflow_json() )

        self.generate_workflow_description()

        # hit batch workflow endpoint if batch values
        if self.batch_values:
            self.id = self.workflow.launch_batch_workflow(self.definition)

        # use regular workflow endpoint if no batch values
        else:
            self.id = self.workflow.launch(self.definition)

        return self.id