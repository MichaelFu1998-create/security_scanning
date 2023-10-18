def _file_type(self, field):
        """ Returns file type for given file field.
        
        Args:
            field (str): File field

        Returns:
            string. File type
        """
        type = mimetypes.guess_type(self._files[field])[0]
        return type.encode("utf-8") if isinstance(type, unicode) else str(type)