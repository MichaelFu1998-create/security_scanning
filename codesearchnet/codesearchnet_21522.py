def _parse_title(self):
        """Parse the title from TeX source.

        Sets these attributes:

        - ``_title``
        - ``_short_title``
        """
        command = LatexCommand(
            'title',
            {'name': 'short_title', 'required': False, 'bracket': '['},
            {'name': 'long_title', 'required': True, 'bracket': '{'})
        try:
            parsed = next(command.parse(self._tex))
        except StopIteration:
            self._logger.warning('lsstdoc has no title')
            self._title = None
            self._short_title = None

        self._title = parsed['long_title']

        try:
            self._short_title = parsed['short_title']
        except KeyError:
            self._logger.warning('lsstdoc has no short title')
            self._short_title = None