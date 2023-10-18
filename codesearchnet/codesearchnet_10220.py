def _keys_to_camel_case(self, obj):
        """
        Make a copy of a dictionary with all keys converted to camel case. This is just calls to_camel_case on each of the keys in the dictionary and returns a new dictionary.

        :param obj: Dictionary to convert keys to camel case.
        :return: Dictionary with the input values and all keys in camel case
        """
        return dict((to_camel_case(key), value) for (key, value) in obj.items())