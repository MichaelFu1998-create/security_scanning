def validate(self, strict=True):
        '''Validate a JAMS object against the schema.

        Parameters
        ----------
        strict : bool
            If `True`, an exception will be raised on validation failure.
            If `False`, a warning will be raised on validation failure.

        Returns
        -------
        valid : bool
            `True` if the object passes schema validation.
            `False` otherwise.

        Raises
        ------
        SchemaError
            If `strict==True` and the JAMS object does not match the schema

        See Also
        --------
        jsonschema.validate

        '''
        valid = True
        try:
            jsonschema.validate(self.__json_light__, schema.JAMS_SCHEMA)

            for ann in self.annotations:
                if isinstance(ann, Annotation):
                    valid &= ann.validate(strict=strict)
                else:
                    msg = '{} is not a well-formed JAMS Annotation'.format(ann)
                    valid = False
                    if strict:
                        raise SchemaError(msg)
                    else:
                        warnings.warn(str(msg))

        except jsonschema.ValidationError as invalid:
            if strict:
                raise SchemaError(str(invalid))
            else:
                warnings.warn(str(invalid))

            valid = False

        return valid