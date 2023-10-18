def get_task(self, id):
        """
        Returns the task with the given id.

        :type id:integer
        :param id: The id of a task.
        :rtype: Task
        :returns: The task with the given id.
        """
        tasks = [task for task in self.get_tasks() if task.id == id]
        return tasks[0] if len(tasks) == 1 else None