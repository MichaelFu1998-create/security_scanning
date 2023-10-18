def deserialize(self, request=None, text=None, format=None):
        """Deserializes the text using a determined deserializer.

        @param[in] request
            The request object to pull information from; normally used to
            determine the deserialization format (when `format` is
            not provided).

        @param[in] text
            The text to be deserialized. Can be left blank and the
            request will be read.

        @param[in] format
            A specific format to deserialize in; if provided, no detection is
            done. If not provided, the content-type header is looked at to
            determine an appropriate deserializer.

        @returns
            A tuple of the deserialized data and an instance of the
            deserializer used.
        """
        if isinstance(self, Resource):
            if not request:
                # Ensure we have a response object.
                request = self._request

        Deserializer = None
        if format:
            # An explicit format was given; do not attempt to auto-detect
            # a deserializer.
            Deserializer = self.meta.deserializers[format]

        if not Deserializer:
            # Determine an appropriate deserializer to use by
            # introspecting the request object and looking at
            # the `Content-Type` header.
            media_ranges = request.get('Content-Type')
            if media_ranges:
                # Parse the media ranges and determine the deserializer
                # that is the closest match.
                media_types = six.iterkeys(self._deserializer_map)
                media_type = mimeparse.best_match(media_types, media_ranges)
                if media_type:
                    format = self._deserializer_map[media_type]
                    Deserializer = self.meta.deserializers[format]

            else:
                # Client didn't provide a content-type; we're supposed
                # to auto-detect.
                # TODO: Implement this.
                pass

        if Deserializer:
            try:
                # Attempt to deserialize the data using the determined
                # deserializer.
                deserializer = Deserializer()
                data = deserializer.deserialize(request=request, text=text)
                return data, deserializer

            except ValueError:
                # Failed to deserialize the data.
                pass

        # Failed to determine a deserializer; or failed to deserialize.
        raise http.exceptions.UnsupportedMediaType()