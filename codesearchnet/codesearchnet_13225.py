def validate(self, strict=True):
        '''Validate a JObject against its schema

        Parameters
        ----------
        strict : bool
            Enforce strict schema validation

        Returns
        -------
        valid : bool
            True if the jam validates
            False if not, and `strict==False`

        Raises
        ------
        SchemaError
            If `strict==True` and `jam` fails validation
        '''

        valid = True

        try:
            jsonschema.validate(self.__json__, self.__schema__)

        except jsonschema.ValidationError as invalid:
            if strict:
                raise SchemaError(str(invalid))
            else:
                warnings.warn(str(invalid))

            valid = False

        return valid