def serialize(self, data, format=None):
        """Serializes the data into this response using a serializer.

        @param[in] data
            The data to be serialized.

        @param[in] format
            A specific format to serialize in; if provided, no detection is
            done. If not provided, the accept header (as well as the URL
            extension) is looked at to determine an appropriate serializer.

        @returns
            A tuple of the serialized text and an instance of the
            serializer used.
        """
        return self._resource.serialize(data, response=self, format=format)