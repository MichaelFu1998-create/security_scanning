def _on_complete(self, my_task):
        """
        Return True on success, False otherwise. Should not be overwritten,
        overwrite _on_complete_hook() instead.

        :type  my_task: Task
        :param my_task: The associated task in the task tree.
        :rtype:  boolean
        :returns: True on success, False otherwise.
        """
        assert my_task is not None

        if my_task.workflow.debug:
            print("Executing %s: %s (%s)" % (
                my_task.task_spec.__class__.__name__,
                my_task.get_name(), my_task.get_description()))

        self._on_complete_hook(my_task)

        # Notify the Workflow.
        my_task.workflow._task_completed_notify(my_task)

        if my_task.workflow.debug:
            if hasattr(my_task.workflow, "outer_workflow"):
                my_task.workflow.outer_workflow.task_tree.dump()

        self.completed_event.emit(my_task.workflow, my_task)
        return True