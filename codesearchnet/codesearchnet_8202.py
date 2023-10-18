def hsv2rgb_rainbow(hsv):
    """Generates RGB values from HSV that have an even visual
    distribution.  Be careful as this method is only have as fast as
    hsv2rgb_spectrum."""

    def nscale8x3_video(r, g, b, scale):
        nonzeroscale = 0
        if scale != 0:
            nonzeroscale = 1
        if r != 0:
            r = ((r * scale) >> 8) + nonzeroscale
        if g != 0:
            g = ((g * scale) >> 8) + nonzeroscale
        if b != 0:
            b = ((b * scale) >> 8) + nonzeroscale
        return (r, g, b)

    def scale8_video_LEAVING_R1_DIRTY(i, scale):
        nonzeroscale = 0
        if scale != 0:
            nonzeroscale = 1
        if i != 0:
            i = ((i * scale) >> 8) + nonzeroscale
        return i

    h, s, v = hsv
    offset = h & 0x1F  # 0..31
    offset8 = offset * 8
    third = (offset8 * (256 // 3)) >> 8
    r, g, b = (0, 0, 0)

    if not (h & 0x80):
        if not (h & 0x40):
            if not (h & 0x20):
                r = 255 - third
                g = third
                b = 0
            else:
                r = 171
                g = 85 + third
                b = 0x00
        else:
            if not (h & 0x20):
                twothirds = (third << 1)
                r = 171 - twothirds
                g = 171 + third
                b = 0
            else:
                r = 0
                g = 255 - third
                b = third
    else:
        if not (h & 0x40):
            if not (h & 0x20):
                r = 0x00
                twothirds = (third << 1)
                g = 171 - twothirds
                b = 85 + twothirds
            else:
                r = third
                g = 0
                b = 255 - third
        else:
            if not (h & 0x20):
                r = 85 + third
                g = 0
                b = 171 - third
            else:
                r = 171 + third
                g = 0x00
                b = 85 - third

    if s != 255:
        r, g, b = nscale8x3_video(r, g, b, s)
        desat = 255 - s
        desat = (desat * desat) >> 8
        brightness_floor = desat
        r = r + brightness_floor
        g = g + brightness_floor
        b = b + brightness_floor

    if v != 255:
        v = scale8_video_LEAVING_R1_DIRTY(v, v)
        r, g, b = nscale8x3_video(r, g, b, v)

    return (r, g, b)