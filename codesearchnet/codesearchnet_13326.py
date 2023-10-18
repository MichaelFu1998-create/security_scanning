def prohibit(self, data):
        """Checks for prohibited characters."""
        for char in data:
            for lookup in self.prohibited:
                if lookup(char):
                    raise StringprepError("Prohibited character: {0!r}"
                                                                .format(char))
        return data