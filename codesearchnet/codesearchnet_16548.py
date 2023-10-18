def set_parameter(self, key, value):
        """
        Set a url parameter.

        Parameters
        ----------
        key : str
            If key ends with '64', the value provided will be automatically
            base64 encoded.
        """
        if value is None or isinstance(value, (int, float, bool)):
            value = str(value)

        if key.endswith('64'):
            value = urlsafe_b64encode(value.encode('utf-8'))
            value = value.replace(b('='), b(''))

        self._parameters[key] = value