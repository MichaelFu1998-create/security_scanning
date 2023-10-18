def _add_notify(self, task_spec):
        """
        Called by a task spec when it was added into the workflow.
        """
        if task_spec.name in self.task_specs:
            raise KeyError('Duplicate task spec name: ' + task_spec.name)
        self.task_specs[task_spec.name] = task_spec
        task_spec.id = len(self.task_specs)