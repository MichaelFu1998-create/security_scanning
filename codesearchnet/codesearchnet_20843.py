def get_part_name(self, undefined=""):
        """
        Args:
            undefined (optional): Argument, which will be returned if the
                      `part_name` record is not found.

        Returns:
            str: Name of the part of the series. or `undefined` if `part_name`\
                 is not found.
        """
        return _undefined_pattern(
            "".join(self.get_subfields("245", "n")),
            lambda x: x.strip() == "",
            undefined
        )