def get_price(self, undefined=""):
        """
        Args:
            undefined (optional): Argument, which will be returned if the
                      `price` record is not found.

        Returns:
            str: Price of the book (with currency) or `undefined` if `price` \
                 is not found.
        """
        return _undefined_pattern(
            "".join(self.get_subfields("020", "c")),
            lambda x: x.strip() == "",
            undefined
        )