def _parse_time(self, tokens):
        """
        Parse the date range for the query

        E.g. WHERE time > now() - 48h AND time < now() - 24h
        would result in DateRange(datetime_start, datetime_end)
        where
        datetime_start would be parsed from now() - 48h
        and
        datetime_end would be parsed from now() - 24h

        :param tokens:
        :return:
        """
        return self.time_parser.parse(self.parse_keyword(Keyword.WHERE, tokens))