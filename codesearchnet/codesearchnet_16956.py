def check(self, query):
        """
        :param query:
        """
        if query.get_type() != Keyword.DELETE:
            return Ok(True)

        return Err("Delete queries are forbidden.")