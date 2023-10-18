def get_publisher(self, undefined=""):
        """
        Args:
            undefined (optional): Argument, which will be returned if the
                      `publisher` record is not found.

        Returns:
            str: Name of the publisher ("``Grada``" for example) or \
                 `undefined` if `publisher` is not found.
        """
        publishers = set([
            remove_hairs_fn(publisher)
            for publisher in self["260b  "] + self["264b"]
        ])

        return _undefined_pattern(
            ", ".join(publishers),
            lambda x: x.strip() == "",
            undefined
        )