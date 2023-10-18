def get_format(self, undefined=""):
        """
        Args:
            undefined (optional): Argument, which will be returned if the
                      `format` record is not found.

        Returns:
            str: Dimensions of the book ('``23 cm``' for example) or 
                `undefined` if `format` is not found.
        """
        return _undefined_pattern(
            "".join(self.get_subfields("300", "c")),
            lambda x: x.strip() == "",
            undefined
        )