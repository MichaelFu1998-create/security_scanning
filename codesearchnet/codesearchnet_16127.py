def add_record_check(self, record_check, modulus=1):
        """
        Add a record check function.

        Arguments
        ---------

        `record_check` - a function that accepts a single argument (a record as
        a dictionary of values indexed by field name) and raises a
        `RecordError` if the record is not valid

        `modulus` - apply the check to every nth record, defaults to 1 (check
        every record)

        """

        assert callable(record_check), 'record check must be a callable function'

        t = record_check, modulus
        self._record_checks.append(t)