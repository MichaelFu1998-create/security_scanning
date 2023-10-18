def _parse_documentclass(self):
        """Parse documentclass options.

        Sets the the ``_document_options`` attribute.
        """
        command = LatexCommand(
            'documentclass',
            {'name': 'options', 'required': False, 'bracket': '['},
            {'name': 'class_name', 'required': True, 'bracket': '{'})
        try:
            parsed = next(command.parse(self._tex))
        except StopIteration:
            self._logger.warning('lsstdoc has no documentclass')
            self._document_options = []

        try:
            content = parsed['options']
            self._document_options = [opt.strip()
                                      for opt in content.split(',')]
        except KeyError:
            self._logger.warning('lsstdoc has no documentclass options')
            self._document_options = []