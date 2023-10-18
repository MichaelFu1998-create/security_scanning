def register(self, task_json=None, json_filename=None):
        """Registers a new GBDX task.

        Args:
            task_json (dict): Dictionary representing task definition.
            json_filename (str): A full path of a file with json representing the task definition.
            Only one out of task_json and json_filename should be provided.
        Returns:
            Response (str).
        """
        if not task_json and not json_filename:
            raise Exception("Both task json and filename can't be none.")

        if task_json and json_filename:
            raise Exception("Both task json and filename can't be provided.")

        if json_filename:
            task_json = json.load(open(json_filename, 'r'))

        r = self.gbdx_connection.post(self._base_url, json=task_json)
        raise_for_status(r)

        return r.text