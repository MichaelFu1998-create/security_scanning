def add_header_check(self,
                         code=HEADER_CHECK_FAILED,
                         message=MESSAGES[HEADER_CHECK_FAILED]):
        """
        Add a header check, i.e., check whether the header record is consistent
        with the expected field names.

        Arguments
        ---------

        `code` - problem code to report if the header record is not valid,
        defaults to `HEADER_CHECK_FAILED`

        `message` - problem message to report if a value is not valid

        """

        t = code, message
        self._header_checks.append(t)