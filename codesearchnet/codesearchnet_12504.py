def list_workflow_outputs(self):
        '''
        Get a list of outputs from the workflow that are saved to S3. To get resolved locations call workflow status.
        Args:
            None

        Returns:
            list
        '''
        workflow_outputs = []
        for task in self.tasks:
            for output_port_name in task.outputs._portnames:
                if task.outputs.__getattribute__(output_port_name).persist:
                    workflow_outputs.append(task.name + ':' + output_port_name)

        return workflow_outputs