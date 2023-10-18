def rgb_to_ansi16(r, g, b, use_bright=False):
    """
    Convert RGB to ANSI 16 color
    """
    ansi_b = round(b / 255.0) << 2
    ansi_g = round(g / 255.0) << 1
    ansi_r = round(r / 255.0)
    ansi = (90 if use_bright else 30) + (ansi_b | ansi_g | ansi_r)

    return ansi