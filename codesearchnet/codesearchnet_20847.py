def get_pub_place(self, undefined=""):
        """
        Args:
            undefined (optional): Argument, which will be returned if the
                      `pub_place` record is not found.

        Returns:
            str: Name of city/country where the book was published or \
                 `undefined` if `pub_place` is not found.
        """
        places = set([
            remove_hairs_fn(place)
            for place in self["260a  "] + self["264a"]
        ])

        return _undefined_pattern(
            ", ".join(places),
            lambda x: x.strip() == "",
            undefined
        )