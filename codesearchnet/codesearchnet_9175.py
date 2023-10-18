def sanitize_color_palette(colorpalette):
    """
    Sanitze the given color palette so it can
    be safely used by Colorful.

    It will convert colors specified in hex RGB to
    a RGB channel triplet.
    """
    new_palette = {}

    def __make_valid_color_name(name):
        """
        Convert the given name into a valid colorname
        """
        if len(name) == 1:
            name = name[0]
            return name[:1].lower() + name[1:]

        return name[0].lower() + ''.join(word.capitalize() for word in name[1:])

    for key, value in colorpalette.items():
        if isinstance(value, str):
            # we assume it's a hex RGB value
            value = utils.hex_to_rgb(value)
        new_palette[__make_valid_color_name(key.split())] = value

    return new_palette