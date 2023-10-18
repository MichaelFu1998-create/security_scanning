def create_from_string(self, string, context=EMPTY_CONTEXT, *args, **kwargs):
        """
        Deserializes a new instance from a string.
        This is a convenience method that creates a StringIO object and calls create_instance_from_stream().
        """
        if not PY2 and not isinstance(string, bytes):
            raise TypeError("string should be an instance of bytes in Python 3")

        io = StringIO(string)
        instance = self.create_from_stream(io, context, *args, **kwargs)
        io.close()
        return instance