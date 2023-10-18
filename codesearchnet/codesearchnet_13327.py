def check_unassigned(self, data):
        """Checks for unassigned character codes."""
        for char in data:
            for lookup in self.unassigned:
                if lookup(char):
                    raise StringprepError("Unassigned character: {0!r}"
                                                                .format(char))
        return data