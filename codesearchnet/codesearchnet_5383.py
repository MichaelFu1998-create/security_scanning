def is_completed(self):
        """
        Returns True if the entire Workflow is completed, False otherwise.

        :rtype: bool
        :return: Whether the workflow is completed.
        """
        mask = Task.NOT_FINISHED_MASK
        iter = Task.Iterator(self.task_tree, mask)
        try:
            next(iter)
        except StopIteration:
            # No waiting tasks found.
            return True
        return False