def load_document(self, id):
        """
        Load a single document by id
        """
        fields = self.redis.hgetall(id)
        if six.PY3:
            f2 = {to_string(k): to_string(v) for k, v in fields.items()}
            fields = f2

        try:
            del fields['id']
        except KeyError:
            pass

        return Document(id=id, **fields)