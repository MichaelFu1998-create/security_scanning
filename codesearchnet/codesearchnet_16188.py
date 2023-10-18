def _unwrap_el(self, value):
        """Convert {'Element': 1234} to WebElement Object

        Args:
            value(str|list|dict): The value field in the json response.

        Returns:
            The unwrapped value.
        """
        if isinstance(value, dict) and 'ELEMENT' in value:
            element_id = value.get('ELEMENT')
            return WebElement(element_id, self)
        elif isinstance(value, list) and not isinstance(value, str):
            return [self._unwrap_el(item) for item in value]
        else:
            return value