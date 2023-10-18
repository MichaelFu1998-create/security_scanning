def get_subname(self, undefined=""):
        """
        Args:
            undefined (optional): Argument, which will be returned if the
                      `subname` record is not found.

        Returns:
            str: Subname of the book or `undefined` if `subname` is not \
                 found.
        """
        return _undefined_pattern(
            "".join(self.get_subfields("245", "b")),
            lambda x: x.strip() == "",
            undefined
        )