def str_to_rgb(self, str):

        """ Returns RGB values based on a descriptive string.

        If the given str is a named color, return its RGB values.
        Otherwise, return a random named color that has str
        in its name, or a random named color which name appears in str.

        Specific suffixes (-ish, -ed, -y and -like) are recognised
        as well, for example, if you need a random variation of "red"
        you can use reddish (or greenish, yellowy, etc.)

        """

        str = str.lower()
        for ch in "_- ":
            str = str.replace(ch, "")

        # if named_hues.has_key(str):
        #    clr = color(named_hues[str], 1, 1, mode="hsb")
        #    return clr.r, clr.g, clr.b

        if named_colors.has_key(str):
            return named_colors[str]

        for suffix in ["ish", "ed", "y", "like"]:
            str = re.sub("(.*?)" + suffix + "$", "\\1", str)
        str = re.sub("(.*?)dd$", "\\1d", str)

        matches = []
        for name in named_colors:
            if name in str or str in name:
                matches.append(named_colors[name])
        if len(matches) > 0:
            return choice(matches)

        return named_colors["transparent"]