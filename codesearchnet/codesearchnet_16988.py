def check(self, query):
        """
        :param query:
        """
        if query.get_type() in {Keyword.LIST, Keyword.DROP}:
            series = query.series_stmt
        else:
            series = query.from_stmt

        if len(series) >= self.min_series_name_length:
            return Ok(True)

        return Err("Series name too short. Please be more precise.")