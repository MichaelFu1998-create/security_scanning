def serialize(self, data, response=None, request=None, format=None):
        """Serializes the data using a determined serializer.

        @param[in] data
            The data to be serialized.

        @param[in] response
            The response object to serialize the data to.
            If this method is invoked as an instance method, the response
            object can be omitted and it will be taken from the instance.

        @param[in] request
            The request object to pull information from; normally used to
            determine the serialization format (when `format` is not provided).
            May be used by some serializers as well to pull additional headers.
            If this method is invoked as an instance method, the request
            object can be omitted and it will be taken from the instance.

        @param[in] format
            A specific format to serialize in; if provided, no detection is
            done. If not provided, the accept header (as well as the URL
            extension) is looked at to determine an appropriate serializer.

        @returns
            A tuple of the serialized text and an instance of the
            serializer used.
        """
        if isinstance(self, Resource):
            if not request:
                # Ensure we have a response object.
                request = self._request

        Serializer = None
        if format:
            # An explicit format was given; do not attempt to auto-detect
            # a serializer.
            Serializer = self.meta.serializers[format]

        if not Serializer:
            # Determine an appropriate serializer to use by
            # introspecting the request object and looking at the `Accept`
            # header.
            media_ranges = (request.get('Accept') or '*/*').strip()
            if not media_ranges:
                # Default the media ranges to */*
                media_ranges = '*/*'

            if media_ranges != '*/*':
                # Parse the media ranges and determine the serializer
                # that is the closest match.
                media_types = six.iterkeys(self._serializer_map)
                media_type = mimeparse.best_match(media_types, media_ranges)
                if media_type:
                    format = self._serializer_map[media_type]
                    Serializer = self.meta.serializers[format]

            else:
                # Client indicated no preference; use the default.
                default = self.meta.default_serializer
                Serializer = self.meta.serializers[default]

        if Serializer:
            try:
                # Attempt to serialize the data using the determined
                # serializer.
                serializer = Serializer(request, response)
                return serializer.serialize(data), serializer

            except ValueError:
                # Failed to serialize the data.
                pass

        # Either failed to determine a serializer or failed to serialize
        # the data; construct a list of available and valid encoders.
        available = {}
        for name in self.meta.allowed_serializers:
            Serializer = self.meta.serializers[name]
            instance = Serializer(request, None)
            if instance.can_serialize(data):
                available[name] = Serializer.media_types[0]

        # Raise a Not Acceptable exception.
        raise http.exceptions.NotAcceptable(available)