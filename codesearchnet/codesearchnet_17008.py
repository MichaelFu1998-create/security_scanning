def parse(self, raw_query_string):
        """
        Parse a raw query string into fields
        :param raw_query_string: Raw InfluxDB query string
        """

        self._reset()

        if not isinstance(raw_query_string, basestring):
            return None

        query_string = self._cleanup(raw_query_string)
        parts = self._split(query_string)
        parts = self._sanitize_keywords(parts)
        tokens = self._tokenize(parts)

        if tokens:
            # Run subparsers to analyze parts of the query
            self.parsed_resolution = self._parse_resolution(tokens)
            self.parsed_time = self._parse_time(tokens)
            self.parsed_time_overlap = self._parse_duration(self.parsed_time)
            self.parsed_datapoints = self._parse_datapoints(
                self.parsed_time_overlap.timespan_seconds(),
                self.parsed_resolution,
                self.parse_keyword(Keyword.LIMIT, tokens)
            )

        return self.create_query_object(tokens)