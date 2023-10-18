def create_select_query(self, tokens):
        """
        Parse tokens of select query
        :param tokens: A list of InfluxDB query tokens
        """
        if not tokens[Keyword.SELECT]:
            return None
        if not tokens[Keyword.FROM]:
            return None

        return SelectQuery(
            self.parse_keyword(Keyword.SELECT, tokens),
            self.parse_keyword(Keyword.FROM, tokens),
            where_stmt=self.parse_keyword(Keyword.WHERE, tokens),
            limit_stmt=self.parse_keyword(Keyword.LIMIT, tokens),
            group_by_stmt=self.parse_group(tokens),
            duration=self.parsed_time_overlap.timespan_seconds(),
            resolution=self.parsed_resolution,
            time_ranges=self.parsed_time,
            time_overlap=self.parsed_time_overlap,
            datapoints=self.parsed_datapoints
        )