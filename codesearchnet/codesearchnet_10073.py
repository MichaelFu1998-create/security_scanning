def cf_dictionary_from_pairs(pairs):
        """
        Creates a CFDictionaryRef object from a list of 2-element tuples
        representing the key and value. Each key should be a CFStringRef and each
        value some sort of CF* type.

        :param pairs:
            A list of 2-element tuples

        :return:
            A CFDictionaryRef
        """

        length = len(pairs)
        keys = []
        values = []
        for pair in pairs:
            key, value = pair
            keys.append(key)
            values.append(value)
        keys = (CFStringRef * length)(*keys)
        values = (CFTypeRef * length)(*values)
        return CoreFoundation.CFDictionaryCreate(
            CoreFoundation.kCFAllocatorDefault,
            _cast_pointer_p(byref(keys)),
            _cast_pointer_p(byref(values)),
            length,
            kCFTypeDictionaryKeyCallBacks,
            kCFTypeDictionaryValueCallBacks
        )