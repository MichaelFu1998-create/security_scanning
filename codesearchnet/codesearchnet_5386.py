def get_tasks_from_spec_name(self, name):
        """
        Returns all tasks whose spec has the given name.

        :type name: str
        :param name: The name of a task spec.
        :rtype: Task
        :return: The task that relates to the spec with the given name.
        """
        return [task for task in self.get_tasks()
                if task.task_spec.name == name]