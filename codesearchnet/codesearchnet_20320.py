def field_metadata(self, well_row=0, well_column=0,
                       field_row=0, field_column=0):
        """Get OME-XML metadata of given field.

        Parameters
        ----------
        well_row : int
            Y well coordinate. Same as --V in files.
        well_column : int
            X well coordinate. Same as --U in files.
        field_row : int
            Y field coordinate. Same as --Y in files.
        field_column : int
            X field coordinate. Same as --X in files.

        Returns
        -------
        lxml.objectify.ObjectifiedElement
            lxml object of OME-XML found in slide/chamber/field/metadata.
        """
        def condition(path):
            attrs = attributes(path)
            return (attrs.u == well_column and attrs.v == well_row
                        and attrs.x == field_column and attrs.y == field_row)

        field = [f for f in self.fields if condition(f)]

        if field:
            field = field[0]
            filename = _pattern(field, 'metadata',
                                _image, extension='*.ome.xml')
            filename = glob(filename)[0] # resolve, assume found
            return objectify.parse(filename).getroot()