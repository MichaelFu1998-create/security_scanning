def _context(self):
        """
        Returns the intersection of each color's context.

        Get the nearest named hue of each color,
        and finds overlapping tags in each hue's colors.
        For example, a list containing yellow, deeppink and olive
        yields: femininity, friendship, happiness, joy.

        """
        tags1 = None
        for clr in self:
            overlap = []
            if clr.is_black:
                name = "black"
            elif clr.is_white:
                name = "white"
            elif clr.is_grey:
                name = "grey"
            else:
                name = clr.nearest_hue(primary=True)
            if name == "orange" and clr.brightness < 0.6:
                name = "brown"
            tags2 = context[name]
            if tags1 is None:
                tags1 = tags2
            else:
                for tag in tags2:
                    if tag in tags1:
                        if tag not in overlap:
                            overlap.append(tag)
                tags1 = overlap

        overlap.sort()
        return overlap