def list(self):
        """Lists the keys
        :return: Returns a list of all keys (not just key names, but rather
        the keys themselves).
        """
        response = self.client.list_objects_v2(Bucket=self.db_path)
        if u'Contents' in response:
            # Filter out everything but the key names
            keys = [key[u'Key'] for key in response[u'Contents']]
            keys_list = []

            for key_name in keys:
                key = self.get(key_name)
                keys_list.append(key)

            return keys_list
        return []