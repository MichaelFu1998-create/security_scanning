def db_value(self, value):
        """
        Convert UUID to binary blob
        """

        # ensure we have a valid UUID
        if not isinstance(value, UUID):
            value = UUID(value)

        # reconstruct for optimal indexing
        parts = str(value).split("-")
        reordered = ''.join([parts[2], parts[1], parts[0], parts[3], parts[4]])
        value = binascii.unhexlify(reordered)
        return super(OrderedUUIDField, self).db_value(value)