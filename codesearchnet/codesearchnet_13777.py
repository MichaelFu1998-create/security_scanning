def is_public(self):
        """Return True iff this class should be considered public."""
        return (
            not self.name.startswith("_")
            and self.parent.is_class
            and self.parent.is_public
        )