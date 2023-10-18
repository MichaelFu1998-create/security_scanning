def _to_json(self, strip, to_serialize=None):
        """Utility function that creates JSON repr. of a credentials object.

        Over-ride is needed since PKCS#12 keys will not in general be JSON
        serializable.

        Args:
            strip: array, An array of names of members to exclude from the
                   JSON.
            to_serialize: dict, (Optional) The properties for this object
                          that will be serialized. This allows callers to
                          modify before serializing.

        Returns:
            string, a JSON representation of this instance, suitable to pass to
            from_json().
        """
        if to_serialize is None:
            to_serialize = copy.copy(self.__dict__)
        pkcs12_val = to_serialize.get(_PKCS12_KEY)
        if pkcs12_val is not None:
            to_serialize[_PKCS12_KEY] = base64.b64encode(pkcs12_val)
        return super(ServiceAccountCredentials, self)._to_json(
            strip, to_serialize=to_serialize)