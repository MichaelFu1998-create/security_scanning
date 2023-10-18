def python_value(self, value):
        """Parse value from database."""
        if self.field_type == 'TEXT' and isinstance(value, str):
            return self.loads(value)
        return value