def cf_string_to_unicode(value):
        """
        Creates a python unicode string from a CFString object

        :param value:
            The CFString to convert

        :return:
            A python unicode string
        """

        string_ptr = CoreFoundation.CFStringGetCStringPtr(
            value,
            kCFStringEncodingUTF8
        )
        string = None if is_null(string_ptr) else ffi.string(string_ptr)
        if string is None:
            buffer = buffer_from_bytes(1024)
            result = CoreFoundation.CFStringGetCString(
                value,
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