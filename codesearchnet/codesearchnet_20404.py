def write(self, chunk, serialize=False, format=None):
        """Writes the given chunk to the output buffer.

        @param[in] chunk
            Either a byte array, a unicode string, or a generator. If `chunk`
            is a generator then calling `self.write(<generator>)` is
            equivalent to:

            @code
                for x in <generator>:
                    self.write(x)
                    self.flush()
            @endcode

        @param[in] serialize
            True to serialize the lines in a determined serializer.

        @param[in] format
            A specific format to serialize in; if provided, no detection is
            done. If not provided, the accept header (as well as the URL
            extension) is looked at to determine an appropriate serializer.
        """

        # Ensure we're not closed.
        self.require_not_closed()

        if chunk is None:
            # There is nothing here.
            return

        if serialize or format is not None:
            # Forward to the serializer to serialize the chunk
            # before it gets written to the response.
            self.serialize(chunk, format=format)
            return  # `serialize` invokes write(...)

        if type(chunk) is six.binary_type:
            # Update the stream length.
            self._length += len(chunk)

            # If passed a byte string, we hope the user encoded it properly.
            self._stream.write(chunk)

        elif isinstance(chunk, six.string_types):
            encoding = self.encoding
            if encoding is not None:
                # If passed a string, we can encode it for the user.
                chunk = chunk.encode(encoding)

            else:
                # Bail; we don't have an encoding.
                raise exceptions.InvalidOperation(
                    'Attempting to write textual data without an encoding.')

            # Update the stream length.
            self._length += len(chunk)

            # Write the encoded data into the byte stream.
            self._stream.write(chunk)

        elif isinstance(chunk, collections.Iterable):
            # If passed some kind of iterator, attempt to recurse into
            # oblivion.
            for section in chunk:
                self.write(section)

        else:
            # Bail; we have no idea what to do with this.
            raise exceptions.InvalidOperation(
                'Attempting to write something not recognized.')