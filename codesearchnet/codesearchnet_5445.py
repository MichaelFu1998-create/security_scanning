def _get_activated_tasks(self, my_task, destination):
        """
        Returns the list of tasks that were activated in the previous
        call of execute(). Only returns tasks that point towards the
        destination task, i.e. those which have destination as a
        descendant.

        my_task -- the task of this TaskSpec
        destination -- the child task
        """
        task = destination._find_ancestor(self.thread_starter)
        return self.thread_starter._get_activated_tasks(task, destination)