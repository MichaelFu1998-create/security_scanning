def value(self):
        """Return the value of the cells."""
        if self.has_value:
            return self._impl[OBJ].get_value(self._impl[KEY])
        else:
            raise ValueError("Value not found")