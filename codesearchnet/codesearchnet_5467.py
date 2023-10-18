def _start(self, my_task, force=False):
        """
        Checks whether the preconditions for going to READY state are met.
        Returns True if the threshold was reached, False otherwise.
        Also returns the list of tasks that yet need to be completed.
        """
        # If the threshold was already reached, there is nothing else to do.
        if my_task._has_state(Task.COMPLETED):
            return True, None
        if my_task._has_state(Task.READY):
            return True, None

        # Check whether we may fire.
        if self.split_task is None:
            return self._check_threshold_unstructured(my_task, force)
        return self._check_threshold_structured(my_task, force)