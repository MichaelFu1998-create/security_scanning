def get_tasks(self):
        """
            Get the tasks attached to the instance

        Returns
        -------
        list
            List of tasks (:class:`asyncio.Task`)
        """
        tasks = self._get_tasks()
        tasks.extend(self._streams.get_tasks(self))

        return tasks