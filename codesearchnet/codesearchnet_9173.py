def parse_rgb_txt_file(path):
    """
    Parse the given rgb.txt file into a Python dict.

    See https://en.wikipedia.org/wiki/X11_color_names for more information

    :param str path: the path to the X11 rgb.txt file
    """
    #: Holds the generated color dict
    color_dict = {}

    with open(path, 'r') as rgb_txt:
        for line in rgb_txt:
            line = line.strip()
            if not line or line.startswith('!'):
                continue  # skip comments

            parts = line.split()
            color_dict[" ".join(parts[3:])] = (int(parts[0]), int(parts[1]), int(parts[2]))

    return color_dict