def present(self, value):
        """Return a user-friendly representation of a value.
        
        Lookup value in self.specials, or call .to_literal() if absent.
        """
        for k, v in self.special.items():
            if v == value:
                return k
        return ''.join(self.get_separator(i) + self.format[i].present(v) for i, v in enumerate(value))