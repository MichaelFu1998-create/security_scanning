def generate_workflow_description(self):
        '''
        Generate workflow json for launching the workflow against the gbdx api

        Args:
            None

        Returns:
            json string
        '''
        if not self.tasks:
            raise WorkflowError('Workflow contains no tasks, and cannot be executed.')

        self.definition = self.workflow_skeleton()

        if self.batch_values:
            self.definition["batch_values"] = self.batch_values

        all_input_port_values = [t.inputs.__getattribute__(input_port_name).value for t in self.tasks for
                                 input_port_name in t.inputs._portnames]
        for task in self.tasks:
            # only include multiplex output ports in this task if other tasks refer to them in their inputs.
            # 1. find the multplex output port_names in this task
            # 2. see if they are referred to in any other tasks inputs
            # 3. If not, exclude them from the workflow_def
            output_multiplex_ports_to_exclude = []
            multiplex_output_port_names = [portname for portname in task.outputs._portnames if
                                           task.outputs.__getattribute__(portname).is_multiplex]
            for p in multiplex_output_port_names:
                output_port_reference = 'source:' + task.name + ':' + p
                if output_port_reference not in all_input_port_values:
                    output_multiplex_ports_to_exclude.append(p)

            task_def = task.generate_task_workflow_json(
                output_multiplex_ports_to_exclude=output_multiplex_ports_to_exclude)
            self.definition['tasks'].append(task_def)

        if self.callback:
            self.definition['callback'] = self.callback

        return self.definition