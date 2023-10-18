def update(self, task_name, task_json):
        """Updates a GBDX task.

        Args:
            task_name (str): Task name.
            task_json (dict): Dictionary representing updated task definition.

        Returns:
            Dictionary representing the updated task definition.
        """
        r = self.gbdx_connection.put(self._base_url + '/' + task_name, json=task_json)
        raise_for_status(r)

        return r.json()