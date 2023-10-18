def list(self):
        """Lists available and visible GBDX tasks.

        Returns:
            List of tasks
        """
        r = self.gbdx_connection.get(self._base_url)
        raise_for_status(r)

        return r.json()['tasks']