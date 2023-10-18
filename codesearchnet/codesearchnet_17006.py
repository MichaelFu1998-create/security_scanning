def check(self, query):
        """
        :param query:
        """
        if query.get_type() not in {Keyword.SELECT}:
            # Bailing out for non select queries
            return Ok(True)

        if query.get_resolution() > 0:
            return Ok(True)

        return Err("Group by statements need a positive time value (e.g. time(10s))")