def add_value_predicate(self, field_name, value_predicate,
                        code=VALUE_PREDICATE_FALSE,
                        message=MESSAGES[VALUE_PREDICATE_FALSE],
                        modulus=1):
        """
        Add a value predicate function for the specified field.

        N.B., everything you can do with value predicates can also be done with
        value check functions, whether you use one or the other is a matter of
        style.

        Arguments
        ---------

        `field_name` - the name of the field to attach the value predicate
        function to

        `value_predicate` - a function that accepts a single argument (a value)
        and returns False if the value is not valid

        `code` - problem code to report if a value is not valid, defaults to
        `VALUE_PREDICATE_FALSE`

        `message` - problem message to report if a value is not valid

        `modulus` - apply the check to every nth record, defaults to 1 (check
        every record)

        """

        assert field_name in self._field_names, 'unexpected field name: %s' % field_name
        assert callable(value_predicate), 'value predicate must be a callable function'

        t = field_name, value_predicate, code, message, modulus
        self._value_predicates.append(t)