def rgb_to_ansi256(r, g, b):
    """
    Convert RGB to ANSI 256 color
    """
    if r == g and g == b:
        if r < 8:
            return 16
        if r > 248:
            return 231

        return round(((r - 8) / 247.0) * 24) + 232

    ansi_r = 36 * round(r / 255.0 * 5.0)
    ansi_g = 6 * round(g / 255.0 * 5.0)
    ansi_b = round(b / 255.0 * 5.0)
    ansi = 16 + ansi_r + ansi_g + ansi_b
    return ansi