def add_value_check(self, field_name, value_check,
                        code=VALUE_CHECK_FAILED,
                        message=MESSAGES[VALUE_CHECK_FAILED],
                        modulus=1):
        """
        Add a value check function for the specified field.

        Arguments
        ---------

        `field_name` - the name of the field to attach the value check function
        to

        `value_check` - a function that accepts a single argument (a value) and
        raises a `ValueError` if the value is not valid

        `code` - problem code to report if a value is not valid, defaults to
        `VALUE_CHECK_FAILED`

        `message` - problem message to report if a value is not valid

        `modulus` - apply the check to every nth record, defaults to 1 (check
        every record)

        """

        # guard conditions
        assert field_name in self._field_names, 'unexpected field name: %s' % field_name
        assert callable(value_check), 'value check must be a callable function'

        t = field_name, value_check, code, message, modulus
        self._value_checks.append(t)