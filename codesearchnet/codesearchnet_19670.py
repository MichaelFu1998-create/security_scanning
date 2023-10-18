def _list_key(self, key):
        """
        boilerplate
        """
        ret = []
        for msg_json in self.client.lrange(key, 0, -1):
            ret.append(self._fromJSON(msg_json))
        return ret