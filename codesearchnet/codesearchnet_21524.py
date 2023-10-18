def _parse_author(self):
        r"""Parse the author from TeX source.

        Sets the ``_authors`` attribute.

        Goal is to parse::

           \author{
           A.~Author,
           B.~Author,
           and
           C.~Author}

        Into::

           ['A. Author', 'B. Author', 'C. Author']
        """
        command = LatexCommand(
            'author',
            {'name': 'authors', 'required': True, 'bracket': '{'})
        try:
            parsed = next(command.parse(self._tex))
        except StopIteration:
            self._logger.warning('lsstdoc has no author')
            self._authors = []
            return

        try:
            content = parsed['authors']
        except KeyError:
            self._logger.warning('lsstdoc has no author')
            self._authors = []
            return

        # Clean content
        content = content.replace('\n', ' ')
        content = content.replace('~', ' ')
        content = content.strip()

        # Split content into list of individual authors
        authors = []
        for part in content.split(','):
            part = part.strip()
            for split_part in part.split('and '):
                split_part = split_part.strip()
                if len(split_part) > 0:
                    authors.append(split_part)
        self._authors = authors