def connect(self, taskspec):
        """
        Connect the *following* task to this one. In other words, the
        given task is added as an output task.

        :type  taskspec: TaskSpec
        :param taskspec: The new output task.
        """
        self.outputs.append(taskspec)
        taskspec._connect_notify(self)