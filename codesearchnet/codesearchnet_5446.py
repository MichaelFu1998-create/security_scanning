def _on_trigger(self, my_task):
        """
        May be called after execute() was already completed to create an
        additional outbound task.
        """
        for output in self.outputs:
            new_task = my_task.add_child(output, Task.READY)
            new_task.triggered = True