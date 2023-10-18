def compound(clr, flip=False):
    """
    Roughly the complement and some far analogs.
    """
    def _wrap(x, min, threshold, plus):
        if x - min < threshold:
            return x + plus
        else:
            return x - min

    d = 1
    if flip: d = -1

    clr = color(clr)
    colors = colorlist(clr)

    c = clr.rotate_ryb(30 * d)
    c.brightness = _wrap(clr.brightness, 0.25, 0.6, 0.25)
    colors.append(c)

    c = clr.rotate_ryb(30 * d)
    c.saturation = _wrap(clr.saturation, 0.4, 0.1, 0.4)
    c.brightness = _wrap(clr.brightness, 0.4, 0.2, 0.4)
    colors.append(c)

    c = clr.rotate_ryb(160 * d)
    c.saturation = _wrap(clr.saturation, 0.25, 0.1, 0.25)
    c.brightness = max(0.2, clr.brightness)
    colors.append(c)

    c = clr.rotate_ryb(150 * d)
    c.saturation = _wrap(clr.saturation, 0.1, 0.8, 0.1)
    c.brightness = _wrap(clr.brightness, 0.3, 0.6, 0.3)
    colors.append(c)

    c = clr.rotate_ryb(150 * d)
    c.saturation = _wrap(clr.saturation, 0.1, 0.8, 0.1)
    c.brightness = _wrap(clr.brightness, 0.4, 0.2, 0.4)
    # colors.append(c)

    return colors