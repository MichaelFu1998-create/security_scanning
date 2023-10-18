def error(self, error_code, value, **kwargs):
        """
        Helper to add error to messages field. It fills placeholder with extra call parameters
        or values from message_value map.

        :param error_code: Error code to use
        :rparam error_code: str
        :param value: Value checked
        :param kwargs: Map of values to use in placeholders
        """
        code = self.error_code_map.get(error_code, error_code)

        try:
            message = Template(self.error_messages[code])
        except KeyError:
            message = Template(self.error_messages[error_code])

        placeholders = {"value": self.hidden_value if self.hidden else value}
        placeholders.update(kwargs)
        placeholders.update(self.message_values)

        self.messages[code] = message.safe_substitute(placeholders)