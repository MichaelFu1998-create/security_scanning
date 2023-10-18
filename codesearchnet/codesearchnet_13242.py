def save(self, path_or_file, strict=True, fmt='auto'):
        """Serialize annotation as a JSON formatted stream to file.

        Parameters
        ----------
        path_or_file : str or file-like
            Path to save the JAMS object on disk
            OR
            An open file descriptor to write into

        strict : bool
            Force strict schema validation

        fmt : str ['auto', 'jams', 'jamz']
            The output encoding format.

            If `auto`, it is inferred from the file name.

            If the input is an open file handle, `jams` encoding
            is used.


        Raises
        ------
        SchemaError
            If `strict == True` and the JAMS object fails schema
            or namespace validation.

        See also
        --------
        validate
        """

        self.validate(strict=strict)

        with _open(path_or_file, mode='w', fmt=fmt) as fdesc:
            json.dump(self.__json__, fdesc, indent=2)