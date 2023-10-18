def get_definition(self, task_name):
        """Gets definition of a registered GBDX task.

        Args:
            task_name (str): Task name.

        Returns:
            Dictionary representing the task definition.
        """
        r = self.gbdx_connection.get(self._base_url + '/' + task_name)
        raise_for_status(r)

        return r.json()