def calculate_uuid(self):
        """Should return a 32-digit hex string for a UUID that is calculated as a function of a set of fields from the model."""

        # raise an error if no inputs to the UUID calculation were specified
        if self.uuid_input_fields is None:
            raise NotImplementedError("""You must define either a 'uuid_input_fields' attribute
                (with a tuple of field names) or override the 'calculate_uuid' method, on models
                that inherit from UUIDModelMixin. If you want a fully random UUID, you can set
                'uuid_input_fields' to the string 'RANDOM'.""")

        # if the UUID has been set to be random, return a random UUID
        if self.uuid_input_fields == "RANDOM":
            return uuid.uuid4().hex

        # if we got this far, uuid_input_fields should be a tuple
        assert isinstance(self.uuid_input_fields, tuple), "'uuid_input_fields' must either be a tuple or the string 'RANDOM'"

        # calculate the input to the UUID function
        hashable_input_vals = []
        for field in self.uuid_input_fields:
            new_value = getattr(self, field)
            if new_value:
                hashable_input_vals.append(str(new_value))
        hashable_input = ":".join(hashable_input_vals)

        # if all the values were falsey, just return a random UUID, to avoid collisions
        if not hashable_input:
            return uuid.uuid4().hex

        # compute the UUID as a function of the input values
        return sha2_uuid(hashable_input)