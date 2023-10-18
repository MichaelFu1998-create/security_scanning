def _on_complete_hook(self, my_task):
        """
        A hook into _on_complete() that does the task specific work.

        :type  my_task: Task
        :param my_task: A task in which this method is executed.
        :rtype:  bool
        :returns: True on success, False otherwise.
        """
        times = int(valueof(my_task, self.times, 1)) + self.queued
        for i in range(times):
            for task_name in self.context:
                task = my_task.workflow.get_task_spec_from_name(task_name)
                task._on_trigger(my_task)
        self.queued = 0
        TaskSpec._on_complete_hook(self, my_task)