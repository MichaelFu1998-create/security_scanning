def nearest_hue(self, primary=False):

        """ Returns the name of the nearest named hue.

        For example,
        if you supply an indigo color (a color between blue and violet),
        the return value is "violet". If primary is set  to True,
        the return value is "purple".

        Primary colors leave out the fuzzy lime, teal,
        cyan, azure and violet hues.

        """
        if self.is_black:
            return "black"
        elif self.is_white:
            return "white"
        elif self.is_grey:
            return "grey"

        if primary:
            hues = primary_hues
        else:
            hues = named_hues.keys()
        nearest, d = "", 1.0
        for hue in hues:
            if abs(self.hue - named_hues[hue]) % 1 < d:
                nearest, d = hue, abs(self.hue - named_hues[hue]) % 1

        return nearest