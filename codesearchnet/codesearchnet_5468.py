def _on_trigger(self, my_task):
        """
        May be called to fire the Join before the incoming branches are
        completed.
        """
        for task in my_task.workflow.task_tree._find_any(self):
            if task.thread_id != my_task.thread_id:
                continue
            self._do_join(task)