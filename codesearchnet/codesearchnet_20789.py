def getDataRecords(self, datafield, subfield, throw_exceptions=True):
        """
        .. deprecated::
            Use :func:`get_subfields` instead.
        """
        return self.get_subfields(
            datafield=datafield,
            subfield=subfield,
            exception=throw_exceptions
        )