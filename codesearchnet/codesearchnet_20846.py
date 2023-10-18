def get_pub_order(self, undefined=""):
        """
        Args:
            undefined (optional): Argument, which will be returned if the
                      `pub_order` record is not found.

        Returns:
            str: Information about order in which was the book published or \
                 `undefined` if `pub_order` is not found.
        """
        return _undefined_pattern(
            "".join(self.get_subfields("901", "f")),
            lambda x: x.strip() == "",
            undefined
        )