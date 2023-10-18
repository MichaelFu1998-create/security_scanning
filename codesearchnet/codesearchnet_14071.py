def monochrome(clr):
    """
    Returns colors in the same hue with varying brightness/saturation.
    """
    def _wrap(x, min, threshold, plus):
        if x - min < threshold:
            return x + plus
        else:
            return x - min

    colors = colorlist(clr)

    c = clr.copy()
    c.brightness = _wrap(clr.brightness, 0.5, 0.2, 0.3)
    c.saturation = _wrap(clr.saturation, 0.3, 0.1, 0.3)
    colors.append(c)

    c = clr.copy()
    c.brightness = _wrap(clr.brightness, 0.2, 0.2, 0.6)
    colors.append(c)

    c = clr.copy()
    c.brightness = max(0.2, clr.brightness + (1 - clr.brightness) * 0.2)
    c.saturation = _wrap(clr.saturation, 0.3, 0.1, 0.3)
    colors.append(c)

    c = clr.copy()
    c.brightness = _wrap(clr.brightness, 0.5, 0.2, 0.3)
    colors.append(c)

    return colors