def _parse_whitespace_argument(source, name):
        r"""Attempt to parse a single token on the first line of this source.

        This method is used for parsing whitespace-delimited arguments, like
        ``\input file``. The source should ideally contain `` file`` along
        with a newline character.

        >>> source = 'Line 1\n' r'\input test.tex' '\nLine 2'
        >>> LatexCommand._parse_whitespace_argument(source, 'input')
        'test.tex'

        Bracket delimited arguments (``\input{test.tex}``) are handled in
        the normal logic of `_parse_command`.
        """
        # First match the command name itself so that we find the argument
        # *after* the command
        command_pattern = r'\\(' + name + r')(?:[\s{[%])'
        command_match = re.search(command_pattern, source)
        if command_match is not None:
            # Trim `source` so we only look after the command
            source = source[command_match.end(1):]

        # Find the whitespace-delimited argument itself.
        pattern = r'(?P<content>\S+)(?:[ %\t\n]+)'
        match = re.search(pattern, source)
        if match is None:
            message = (
                'When parsing {}, did not find whitespace-delimited command '
                'argument'
            )
            raise CommandParserError(message.format(name))
        content = match.group('content')
        content.strip()
        return content