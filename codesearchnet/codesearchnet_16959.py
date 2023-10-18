def check(self, query):
        """
        :param query:
        """
        if query.get_type() not in {Keyword.SELECT, Keyword.DELETE}:
            # Only select and delete queries deal with time durations
            # All others are not affected by this rule. Bailing out.
            return Ok(True)

        datapoints = query.get_datapoints()
        if datapoints <= self.max_datapoints:
            return Ok(True)

        return Err(("Expecting {} datapoints from that query, which is above the threshold! "
                    "Set a date range (e.g. where time > now() - 24h), "
                    "increase grouping (e.g. group by time(24h) "
                    "or limit the number of datapoints (e.g. limit 100)").format(datapoints))