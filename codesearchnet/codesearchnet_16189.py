def _wrap_el(self, value):
        """Convert WebElement Object to {'Element': 1234}

        Args:
            value(str|list|dict): The local value.

        Returns:
            The wrapped value.
        """
        if isinstance(value, dict):
            return {k: self._wrap_el(v) for k, v in value.items()}
        elif isinstance(value, WebElement):
            return {'ELEMENT': value.element_id}
        elif isinstance(value, list) and not isinstance(value, str):
            return [self._wrap_el(item) for item in value]
        else:
            return value