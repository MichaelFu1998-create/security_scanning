def _parse_resolution(self, tokens):
        """
        Parse resolution from the GROUP BY statement.
        E.g. GROUP BY time(10s) would mean a 10 second resolution
        :param tokens:
        :return:
        """
        return self.resolution_parser.parse(self.parse_keyword(Keyword.GROUP_BY, tokens))