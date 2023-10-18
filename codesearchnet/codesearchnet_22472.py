def set_value(self, value, timeout):
        """
        Changes the cached value and updates creation time.
        
        Args:
            value: the new cached value.
            timeout: time to live for the object in milliseconds

        Returns: None
        """
        self.value = value
        self.expiration = time.clock() * 1000 + timeout