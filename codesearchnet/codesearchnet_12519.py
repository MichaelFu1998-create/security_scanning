def delete(self, task_name):
        """Deletes a GBDX task.

        Args:
            task_name (str): Task name.

        Returns:
            Response (str).
        """
        r = self.gbdx_connection.delete(self._base_url + '/' + task_name)
        raise_for_status(r)

        return r.text