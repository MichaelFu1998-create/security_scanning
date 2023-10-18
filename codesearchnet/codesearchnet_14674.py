def put(self, key):
        """Insert the key
        :return: Key name
        """
        self.client.put_object(
            Body=json.dumps(key),
            Bucket=self.db_path,
            Key=key['name'])
        return key['name']