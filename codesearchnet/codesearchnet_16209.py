def raise_for_status(self):
        """Raise WebDriverException if returned status is not zero."""
        if not self.status:
            return

        error = find_exception_by_code(self.status)
        message = None
        screen = None
        stacktrace = None

        if isinstance(self.value, str):
            message = self.value
        elif isinstance(self.value, dict):
            message = self.value.get('message', None)
            screen = self.value.get('screen', None)
            stacktrace = self.value.get('stacktrace', None)

        raise WebDriverException(error, message, screen, stacktrace)