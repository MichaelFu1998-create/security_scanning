def present(self, value):
        """Return a user-friendly representation of a value.
        
        Lookup value in self.specials, or call .to_literal() if absent.
        """
        for k, v in self.special.items():
            if v == value:
                return k
        return self.separator.join(self.format.present(v) for v in value)