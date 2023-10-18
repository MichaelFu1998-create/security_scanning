def create_drop_query(self, tokens):
        """
        Parse tokens of drop query
        :param tokens: A list of InfluxDB query tokens
        """
        if not tokens[Keyword.SERIES]:
            return None
        return DropQuery(self.parse_keyword(Keyword.SERIES, tokens))