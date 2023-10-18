def read(self, deserialize=False, format=None):
        """Read and return the request data.

        @param[in] deserialize
            True to deserialize the resultant text using a determiend format
            or the passed format.

        @param[in] format
            A specific format to deserialize in; if provided, no detection is
            done. If not provided, the content-type header is looked at to
            determine an appropriate deserializer.
        """

        if deserialize:
            data, _ = self.deserialize(format=format)
            return data

        content = self._read()

        if not content:
            return ''

        if type(content) is six.binary_type:
            content = content.decode(self.encoding)

        return content