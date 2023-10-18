def connect_if(self, condition, task_spec):
        """
        Connects a taskspec that is executed if the condition DOES match.

        condition -- a condition (Condition)
        taskspec -- the conditional task spec
        """
        assert task_spec is not None
        self.outputs.append(task_spec)
        self.cond_task_specs.append((condition, task_spec.name))
        task_spec._connect_notify(self)