def get_part(self, undefined=""):
        """
        Args:
            undefined (optional): Argument, which will be returned if the
                      `part` record is not found.

        Returns:
            str: Which part of the book series is this record or `undefined` \
                 if `part` is not found.
        """
        return _undefined_pattern(
            "".join(self.get_subfields("245", "p")),
            lambda x: x.strip() == "",
            undefined
        )