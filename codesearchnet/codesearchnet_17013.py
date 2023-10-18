def create_delete_query(self, tokens):
        """
        Parse tokens of delete query
        :param tokens: A list of InfluxDB query tokens
        """
        # From keyword is required
        if not tokens[Keyword.FROM]:
            return None
        where_stmt = self.parse_keyword(Keyword.WHERE, tokens)
        if where_stmt:
            if not where_stmt.startswith('time'):
                return None
        return DeleteQuery(
            self.parse_keyword(Keyword.FROM, tokens),
            self.parse_keyword(Keyword.WHERE, tokens)
        )