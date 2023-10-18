def add_unique_check(self, key,
                        code=UNIQUE_CHECK_FAILED,
                        message=MESSAGES[UNIQUE_CHECK_FAILED]):
        """
        Add a unique check on a single column or combination of columns.

        Arguments
        ---------

        `key` - a single field name (string) specifying a field in which all
        values are expected to be unique, or a sequence of field names (tuple
        or list of strings) specifying a compound key

        `code` - problem code to report if a record is not valid, defaults to
        `UNIQUE_CHECK_FAILED`

        `message` - problem message to report if a record is not valid

        """

        if isinstance(key, basestring):
            assert key in self._field_names, 'unexpected field name: %s' % key
        else:
            for f in key:
                assert f in self._field_names, 'unexpected field name: %s' % key
        t = key, code, message
        self._unique_checks.append(t)