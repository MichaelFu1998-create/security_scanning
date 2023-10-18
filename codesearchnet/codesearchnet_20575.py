def get_attributes(self, attributes, default=''):
        """Return the attributes values from this DicomFile

        Parameters
        ----------
        attributes: str or list of str
         DICOM field names

        default: str
         Default value if the attribute does not exist.

        Returns
        -------
        Value of the field or list of values.
        """
        if isinstance(attributes, str):
            attributes = [attributes]

        attrs = [getattr(self, attr, default) for attr in attributes]

        if len(attrs) == 1:
            return attrs[0]

        return tuple(attrs)