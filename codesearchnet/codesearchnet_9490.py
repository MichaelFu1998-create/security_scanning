def parse_list_line(self, b):
        """
        Parse LIST response with both Microsoft Windows® parser and
        UNIX parser

        :param b: response line
        :type b: :py:class:`bytes` or :py:class:`str`

        :return: (path, info)
        :rtype: (:py:class:`pathlib.PurePosixPath`, :py:class:`dict`)
        """
        ex = []
        parsers = (self.parse_list_line_unix, self.parse_list_line_windows)
        for parser in parsers:
            try:
                return parser(b)
            except (ValueError, KeyError, IndexError) as e:
                ex.append(e)
        raise ValueError("All parsers failed to parse", b, ex)