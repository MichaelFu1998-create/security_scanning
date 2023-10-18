def order_error(self, first_tag, second_tag, line):
        """Reports an OrderError. Error message will state that
        first_tag came before second_tag.
        """
        self.error = True
        msg = ERROR_MESSAGES['A_BEFORE_B'].format(first_tag, second_tag, line)
        self.logger.log(msg)