def cf_string_to_unicode(value):
        """
        Creates a python unicode string from a CFString object

        :param value:
            The CFString to convert

        :return:
            A python unicode string
        """

        string = CoreFoundation.CFStringGetCStringPtr(
            _cast_pointer_p(value),
            kCFStringEncodingUTF8
        )
        if string is None:
            buffer = buffer_from_bytes(1024)
            result = CoreFoundation.CFStringGetCString(
                _cast_pointer_p(value),
                buffer,
                1024,
                kCFStringEncodingUTF8
            )
            if not result:
                raise OSError('Error copying C string from CFStringRef')
            string = byte_string_from_buffer(buffer)
        if string is not None:
            string = string.decode('utf-8')
        return string