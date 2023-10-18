def validate(self, messages):
        """Returns True if the fields are valid according to the SPDX standard.
        Appends user friendly messages to the messages parameter.
        """
        messages = self.validate_creators(messages)
        messages = self.validate_created(messages)

        return messages