def get_user_info(self):
        """Return readable string."""
        if self.value in ERROR_DESCRIPTIONS:
            s = "{}".format(ERROR_DESCRIPTIONS[self.value])
        else:
            s = "{}".format(self.value)

        if self.context_info:
            s += ": {}".format(self.context_info)
        elif self.value in ERROR_RESPONSES:
            s += ": {}".format(ERROR_RESPONSES[self.value])

        if self.src_exception:
            s += "\n    Source exception: '{}'".format(self.src_exception)

        if self.err_condition:
            s += "\n    Error condition: '{}'".format(self.err_condition)
        return s