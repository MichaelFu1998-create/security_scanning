def cf_dictionary_to_dict(dictionary):
        """
        Converts a CFDictionary object into a python dictionary

        :param dictionary:
            The CFDictionary to convert

        :return:
            A python dict
        """

        dict_length = CoreFoundation.CFDictionaryGetCount(dictionary)

        keys = (CFTypeRef * dict_length)()
        values = (CFTypeRef * dict_length)()
        CoreFoundation.CFDictionaryGetKeysAndValues(
            dictionary,
            _cast_pointer_p(keys),
            _cast_pointer_p(values)
        )

        output = {}
        for index in range(0, dict_length):
            output[CFHelpers.native(keys[index])] = CFHelpers.native(values[index])

        return output