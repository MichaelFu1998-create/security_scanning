def create_list_query(self, tokens):
        """
        Parse tokens of list query
        :param tokens: A list of InfluxDB query tokens
        """
        if not tokens[Keyword.SERIES]:
            # A list series keyword is allowed
            # without a series name or regex
            tokens[Keyword.SERIES] = ''
        return ListQuery(self.parse_keyword(Keyword.SERIES, tokens))