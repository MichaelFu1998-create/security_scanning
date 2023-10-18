def text_color(background, dark_color=rgb_min, light_color=rgb_max):
    """
    Given a background color in the form of an RGB 3-tuple, returns the color the text should be (defaulting to white
    and black) for best readability. The light (white) and dark (black) defaults can be overridden to return preferred
    values.

    :param background:
    :param dark_color:
    :param light_color:
    :return:
    """
    max_y = rgb_to_yiq(rgb_max)[0]
    return light_color if rgb_to_yiq(background)[0] <= max_y / 2 else dark_color