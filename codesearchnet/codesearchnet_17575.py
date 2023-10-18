def calculate(self, **state):
        """
        Base calculate method for models.
        Validates the material state parameter(s).

        :param **state: The material state
        """
        if not self.state_validator.validate(state):
            msg = f"{self.material} {self.property} model. The state "
            msg += f"description ({state}) contains errors:"
            for key, value in self.state_validator.errors.items():
                msg += ' %s: %s;' % (key, value)
            msg = msg[0:-1]+'.'
            raise ValidationError(msg)