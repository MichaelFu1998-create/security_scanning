def add_color_to_scheme(scheme, name, foreground, background, palette_colors):
    """Add foreground and background colours to a color scheme"""
    if foreground is None and background is None:
        return scheme

    new_scheme = []
    for item in scheme:
        if item[0] == name:
            if foreground is None:
                foreground = item[1]
            if background is None:
                background = item[2]
            if palette_colors > 16:
                new_scheme.append((name, '', '', '', foreground, background))
            else:
                new_scheme.append((name, foreground, background))
        else:
            new_scheme.append(item)
    return new_scheme