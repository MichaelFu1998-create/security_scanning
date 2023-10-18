def connect(self, task_spec):
        """
        Connects the task spec that is executed if no other condition
        matches.

        :type  task_spec: TaskSpec
        :param task_spec: The following task spec.
        """
        assert self.default_task_spec is None
        self.outputs.append(task_spec)
        self.default_task_spec = task_spec.name
        task_spec._connect_notify(self)