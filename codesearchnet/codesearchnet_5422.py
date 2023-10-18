def _predict(self, my_task, seen=None, looked_ahead=0):
        """
        Updates the branch such that all possible future routes are added.

        Should NOT be overwritten! Instead, overwrite _predict_hook().

        :type  my_task: Task
        :param my_task: The associated task in the task tree.
        :type  seen: list[taskspec]
        :param seen: A list of already visited tasks.
        :type  looked_ahead: integer
        :param looked_ahead: The depth of the predicted path so far.
        """
        if my_task._is_finished():
            return
        if seen is None:
            seen = []
        elif self in seen:
            return
        if not my_task._is_finished():
            self._predict_hook(my_task)
        if not my_task._is_definite():
            if looked_ahead + 1 >= self.lookahead:
                return
            seen.append(self)
        for child in my_task.children:
            child.task_spec._predict(child, seen[:], looked_ahead + 1)