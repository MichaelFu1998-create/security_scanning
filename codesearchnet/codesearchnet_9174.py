def parse_json_color_file(path):
    """Parse a JSON color file.

    The JSON has to be in the following format:

    .. code:: json

       [{"name": "COLOR_NAME", "hex": "#HEX"}, ...]

    :param str path: the path to the JSON color file
    """
    with open(path, "r") as color_file:
        color_list = json.load(color_file)

    # transform raw color list into color dict
    color_dict = {c["name"]: c["hex"] for c in color_list}
    return color_dict