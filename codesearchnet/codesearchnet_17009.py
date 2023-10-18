def create_query_object(self, tokens):
        """
        Analyze query tokens and create an InfluxDBStatement from them
        Return None on error
        :param tokens: A list of InfluxDB query tokens
        """
        try:
            query_type = tokens['type']
            return getattr(self, 'create_%s_query' % query_type)(tokens)
        except (KeyError, TypeError):
            return self.invalid_query(tokens)