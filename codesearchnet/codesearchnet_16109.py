def value_to_string(self, obj):
        """Pickled data is serialized as base64"""
        value = self.value_from_object(obj)
        return b64encode(self._dump(value)).decode('ascii')