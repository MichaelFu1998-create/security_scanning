def _on_ready(self, my_task):
        """
        Return True on success, False otherwise.

        :type  my_task: Task
        :param my_task: The associated task in the task tree.
        """
        assert my_task is not None
        self.test()

        # Acquire locks, if any.
        for lock in self.locks:
            mutex = my_task.workflow._get_mutex(lock)
            if not mutex.testandset():
                return

        # Assign variables, if so requested.
        for assignment in self.pre_assign:
            assignment.assign(my_task, my_task)

        # Run task-specific code.
        self._on_ready_before_hook(my_task)
        self.reached_event.emit(my_task.workflow, my_task)
        self._on_ready_hook(my_task)

        # Run user code, if any.
        if self.ready_event.emit(my_task.workflow, my_task):
            # Assign variables, if so requested.
            for assignment in self.post_assign:
                assignment.assign(my_task, my_task)

        # Release locks, if any.
        for lock in self.locks:
            mutex = my_task.workflow._get_mutex(lock)
            mutex.unlock()

        self.finished_event.emit(my_task.workflow, my_task)