def python_value(self, value):
        """Convert the database value to a pythonic value."""
        value = coerce_to_bytes(value)
        obj = HashValue(value)
        obj.field = self
        return obj