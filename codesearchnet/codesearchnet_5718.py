def _to_json(self, strip, to_serialize=None):
        """Utility function that creates JSON repr. of a Credentials object.

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
        curr_type = self.__class__
        if to_serialize is None:
            to_serialize = copy.copy(self.__dict__)
        else:
            # Assumes it is a str->str dictionary, so we don't deep copy.
            to_serialize = copy.copy(to_serialize)
        for member in strip:
            if member in to_serialize:
                del to_serialize[member]
        to_serialize['token_expiry'] = _parse_expiry(
            to_serialize.get('token_expiry'))
        # Add in information we will need later to reconstitute this instance.
        to_serialize['_class'] = curr_type.__name__
        to_serialize['_module'] = curr_type.__module__
        for key, val in to_serialize.items():
            if isinstance(val, bytes):
                to_serialize[key] = val.decode('utf-8')
            if isinstance(val, set):
                to_serialize[key] = list(val)
        return json.dumps(to_serialize)