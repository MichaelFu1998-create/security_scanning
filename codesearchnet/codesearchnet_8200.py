def hsv2rgb_raw(hsv):
    """
    Converts an HSV tuple to RGB. Intended for internal use.
    You should use hsv2rgb_spectrum or hsv2rgb_rainbow instead.
    """

    HSV_SECTION_3 = 0x40

    h, s, v = hsv

    # The brightness floor is minimum number that all of
    # R, G, and B will be set to.
    invsat = 255 - s
    brightness_floor = (v * invsat) // 256

    # The color amplitude is the maximum amount of R, G, and B
    # that will be added on top of the brightness_floor to
    # create the specific hue desired.
    color_amplitude = v - brightness_floor

    # figure out which section of the hue wheel we're in,
    # and how far offset we are within that section
    section = h // HSV_SECTION_3  # 0..2
    offset = h % HSV_SECTION_3  # 0..63

    rampup = offset
    rampdown = (HSV_SECTION_3 - 1) - offset

    # compute color-amplitude-scaled-down versions of rampup and rampdown
    rampup_amp_adj = (rampup * color_amplitude) // (256 // 4)
    rampdown_amp_adj = (rampdown * color_amplitude) // (256 // 4)

    # add brightness_floor offset to everything
    rampup_adj_with_floor = rampup_amp_adj + brightness_floor
    rampdown_adj_with_floor = rampdown_amp_adj + brightness_floor

    r, g, b = (0, 0, 0)

    if section:
        if section == 1:
            # section 1: 0x40..0x7F
            r = brightness_floor
            g = rampdown_adj_with_floor
            b = rampup_adj_with_floor
        else:
            # section 2; 0x80..0xBF
            r = rampup_adj_with_floor
            g = brightness_floor
            b = rampdown_adj_with_floor
    else:
        # section 0: 0x00..0x3F
        r = rampdown_adj_with_floor
        g = rampup_adj_with_floor
        b = brightness_floor

    return (r, g, b)