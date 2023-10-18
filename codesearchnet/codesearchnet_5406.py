def _ready(self):
        """
        Marks the task as ready for execution.
        """
        if self._has_state(self.COMPLETED) or self._has_state(self.CANCELLED):
            return
        self._set_state(self.READY)
        self.task_spec._on_ready(self)