def _parse_doc_ref(self):
        """Parse the document handle.

        Sets the ``_series``, ``_serial``, and ``_handle`` attributes.
        """
        command = LatexCommand(
            'setDocRef',
            {'name': 'handle', 'required': True, 'bracket': '{'})
        try:
            parsed = next(command.parse(self._tex))
        except StopIteration:
            self._logger.warning('lsstdoc has no setDocRef')
            self._handle = None
            self._series = None
            self._serial = None
            return

        self._handle = parsed['handle']
        try:
            self._series, self._serial = self._handle.split('-', 1)
        except ValueError:
            self._logger.warning('lsstdoc handle cannot be parsed into '
                                 'series and serial: %r', self._handle)
            self._series = None
            self._serial = None