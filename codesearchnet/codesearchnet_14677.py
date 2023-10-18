def delete(self, key_name):
        """Delete the key.
        :return: True if it was deleted, False otherwise
        """
        self.client.delete_object(
            Bucket=self.db_path,
            Key=key_name)

        return self.get(key_name) == {}