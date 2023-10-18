def new_from_json(cls, json_data):
        """Utility class method to instantiate a Credentials subclass from JSON.

        Expects the JSON string to have been produced by to_json().

        Args:
            json_data: string or bytes, JSON from to_json().

        Returns:
            An instance of the subclass of Credentials that was serialized with
            to_json().
        """
        json_data_as_unicode = _helpers._from_bytes(json_data)
        data = json.loads(json_data_as_unicode)
        # Find and call the right classmethod from_json() to restore
        # the object.
        module_name = data['_module']
        try:
            module_obj = __import__(module_name)
        except ImportError:
            # In case there's an object from the old package structure,
            # update it
            module_name = module_name.replace('.googleapiclient', '')
            module_obj = __import__(module_name)

        module_obj = __import__(module_name,
                                fromlist=module_name.split('.')[:-1])
        kls = getattr(module_obj, data['_class'])
        return kls.from_json(json_data_as_unicode)