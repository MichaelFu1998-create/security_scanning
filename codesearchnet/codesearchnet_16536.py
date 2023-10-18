def export(self, filename, file_format=None, type=None, typequote='"'):
        """export density to file using the given format.

        The format can also be deduced from the suffix of the filename
        though the *format* keyword takes precedence.

        The default format for export() is 'dx'.  Use 'dx' for
        visualization.

        Implemented formats:

        dx
            :mod:`OpenDX`
        pickle
            pickle (use :meth:`Grid.load` to restore); :meth:`Grid.save`
            is simpler than ``export(format='python')``.

        Parameters
        ----------

        filename : str
            name of the output file

        file_format : {'dx', 'pickle', None} (optional)
            output file format, the default is "dx"

        type : str (optional)
            for DX, set the output DX array type, e.g., "double" or "float".
            By default (``None``), the DX type is determined from the numpy
            dtype of the array of the grid (and this will typically result in
            "double").

            .. versionadded:: 0.4.0

        typequote : str (optional)
            For DX, set the character used to quote the type string;
            by default this is a double-quote character, '"'.
            Custom parsers like the one from NAMD-GridForces (backend for MDFF)
            expect no quotes, and typequote='' may be used to appease them.

            .. versionadded:: 0.5.0

        """
        exporter = self._get_exporter(filename, file_format=file_format)
        exporter(filename, type=type, typequote=typequote)