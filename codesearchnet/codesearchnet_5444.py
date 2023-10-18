def connect(self, task_spec):
        """
        Connect the *following* task to this one. In other words, the
        given task is added as an output task.

        task -- the task to connect to.
        """
        self.thread_starter.outputs.append(task_spec)
        task_spec._connect_notify(self.thread_starter)