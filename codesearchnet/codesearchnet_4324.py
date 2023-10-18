def value_error(self, key, bad_value):
        """Reports a value error using ERROR_MESSAGES dict.
        key - key to use for ERROR_MESSAGES.
        bad_value - is passed to format which is called on what key maps to
        in ERROR_MESSAGES.
        """
        msg = ERROR_MESSAGES[key].format(bad_value)
        self.logger.log(msg)
        self.error = True