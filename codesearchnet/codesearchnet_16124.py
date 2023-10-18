def add_record_length_check(self,
                         code=RECORD_LENGTH_CHECK_FAILED,
                         message=MESSAGES[RECORD_LENGTH_CHECK_FAILED],
                         modulus=1):
        """
        Add a record length check, i.e., check whether the length of a record is
        consistent with the number of expected fields.

        Arguments
        ---------

        `code` - problem code to report if a record is not valid, defaults to
        `RECORD_LENGTH_CHECK_FAILED`

        `message` - problem message to report if a record is not valid

        `modulus` - apply the check to every nth record, defaults to 1 (check
        every record)

        """

        t = code, message, modulus
        self._record_length_checks.append(t)