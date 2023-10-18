def check(self, query):
        """
        :param query:
        """
        if query.get_type() not in {Keyword.SELECT}:
            # Only select queries need to be checked here
            # All others are not affected by this rule. Bailing out.
            return Ok(True)

        earliest_date = query.get_earliest_date()
        if earliest_date >= self.min_start_date:
            return Ok(True)

        if query.limit_stmt:
            return Ok(True)

        return Err(("Querying for data before {} is prohibited. "
                    "Your beginning date is {}, which is before that.").format(self.min_start_date.strftime("%Y-%m-%d"),
                                                                              earliest_date))