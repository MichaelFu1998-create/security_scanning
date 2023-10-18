def default(self, obj):
        """
        Convert an object to a form ready to dump to json.

        :param obj: Object being serialized. The type of this object must be one of the following: None; a single object derived from the Pio class; or a list of objects, each derived from the Pio class.
        :return: List of dictionaries, each representing a physical information object, ready to be serialized.
        """
        if obj is None:
            return []
        elif isinstance(obj, list):
            return [i.as_dictionary() for i in obj]
        elif isinstance(obj, dict):
            return self._keys_to_camel_case(obj)
        else:
            return obj.as_dictionary()