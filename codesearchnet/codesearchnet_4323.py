def more_than_one_error(self, field):
        """Logs a more than one error.
        field is the field/property that has more than one defined.
        """
        msg = 'More than one {0} defined.'.format(field)
        self.logger.log(msg)
        self.error = True