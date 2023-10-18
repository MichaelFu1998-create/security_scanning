def _read_file(self):
        """
        read the db file content
        :rtype: dict
        """
        if not os.path.exists(self.db_path):
            return {}
        with open(self.db_path, 'r') as f:
            content = f.read()
            return json.loads(content)