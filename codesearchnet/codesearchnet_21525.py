def _parse_abstract(self):
        """Parse the abstract from the TeX source.

        Sets the ``_abstract`` attribute.
        """
        command = LatexCommand(
            'setDocAbstract',
            {'name': 'abstract', 'required': True, 'bracket': '{'})
        try:
            parsed = next(command.parse(self._tex))
        except StopIteration:
            self._logger.warning('lsstdoc has no abstract')
            self._abstract = None
            return

        try:
            content = parsed['abstract']
        except KeyError:
            self._logger.warning('lsstdoc has no abstract')
            self._abstract = None
            return

        content = content.strip()
        self._abstract = content