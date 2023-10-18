def parse_colors(path):
    """Parse the given color files.

    Supported are:
        * .txt for X11 colors
        * .json for colornames
    """
    if path.endswith(".txt"):
        return parse_rgb_txt_file(path)
    elif path.endswith(".json"):
        return parse_json_color_file(path)

    raise TypeError("colorful only supports .txt and .json files for colors")