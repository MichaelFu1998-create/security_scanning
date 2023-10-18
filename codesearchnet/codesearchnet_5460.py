def get_ready_user_tasks(self):
        """
        Returns a list of User Tasks that are READY for user action
        """
        return [t for t in self.get_tasks(Task.READY)
                if not self._is_engine_task(t.task_spec)]