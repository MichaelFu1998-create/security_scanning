def accept_message(self, message):
        """
        Indicate to the workflow that a message has been received. The message
        will be processed by any waiting Intermediate or Boundary Message
        Events, that are waiting for the message.
        """
        assert not self.read_only
        self.refresh_waiting_tasks()
        self.do_engine_steps()
        for my_task in Task.Iterator(self.task_tree, Task.WAITING):
            my_task.task_spec.accept_message(my_task, message)