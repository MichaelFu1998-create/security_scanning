def default_decoder(self, obj):
        """Handle a dict that might contain a wrapped state for a custom type."""
        typename, marshalled_state = self.unwrap_callback(obj)
        if typename is None:
            return obj

        try:
            cls, unmarshaller = self.serializer.unmarshallers[typename]
        except KeyError:
            raise LookupError('no unmarshaller found for type "{}"'.format(typename)) from None

        if cls is not None:
            instance = cls.__new__(cls)
            unmarshaller(instance, marshalled_state)
            return instance
        else:
            return unmarshaller(marshalled_state)