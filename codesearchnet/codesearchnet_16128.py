def add_record_predicate(self, record_predicate,
                        code=RECORD_PREDICATE_FALSE,
                        message=MESSAGES[RECORD_PREDICATE_FALSE],
                        modulus=1):
        """
        Add a record predicate function.

        N.B., everything you can do with record predicates can also be done with
        record check functions, whether you use one or the other is a matter of
        style.

        Arguments
        ---------

        `record_predicate` - a function that accepts a single argument (a record
        as a dictionary of values indexed by field name) and returns False if
        the value is not valid

        `code` - problem code to report if a record is not valid, defaults to
        `RECORD_PREDICATE_FALSE`

        `message` - problem message to report if a record is not valid

        `modulus` - apply the check to every nth record, defaults to 1 (check
        every record)

        """

        assert callable(record_predicate), 'record predicate must be a callable function'

        t = record_predicate, code, message, modulus
        self._record_predicates.append(t)