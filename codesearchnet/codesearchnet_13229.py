def validate(self, strict=True):
        '''Validate this annotation object against the JAMS schema,
        and its data against the namespace schema.

        Parameters
        ----------
        strict : bool
            If `True`, then schema violations will cause an Exception.
            If `False`, then schema violations will issue a warning.

        Returns
        -------
        valid : bool
            `True` if the object conforms to schema.
            `False` if the object fails to conform to schema,
            but `strict == False`.

        Raises
        ------
        SchemaError
            If `strict == True` and the object fails validation

        See Also
        --------
        JObject.validate
        '''

        # Get the schema for this annotation
        ann_schema = schema.namespace_array(self.namespace)

        valid = True

        try:
            jsonschema.validate(self.__json_light__(data=False),
                                schema.JAMS_SCHEMA)

            # validate each record in the frame
            data_ser = [serialize_obj(obs) for obs in self.data]
            jsonschema.validate(data_ser, ann_schema)

        except jsonschema.ValidationError as invalid:
            if strict:
                raise SchemaError(str(invalid))
            else:
                warnings.warn(str(invalid))
            valid = False

        return valid