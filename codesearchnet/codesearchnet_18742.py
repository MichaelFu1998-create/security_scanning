def size_to_nearest(width=None, height=None, allowed_sizes=OEMBED_ALLOWED_SIZES,
                    force_fit=False):
    """
    Generate some dimensions for resizing an object.  This function DOES NOT handle
    scaling, it simply calculates maximums.  These values should then be passed to
    the resize() method which will scale it and return the scaled width & height.
    """
    minwidth, minheight = min(allowed_sizes)
    maxwidth, maxheight = max(allowed_sizes)

    if not width and not height:
        return maxwidth, maxheight

    if width:
        width = int(width) > minwidth and int(width) or minwidth
    elif force_fit:
        width = maxwidth

    if height:
        height = int(height) > minheight and int(height) or minheight
    elif force_fit:
        height = maxheight

    for size in sorted(allowed_sizes):
        if width and not height:
            if width >= size[0]:
                maxwidth = size[0]
                if force_fit:
                    maxheight = size[1]
            else:
                break
        elif height and not width:
            if height >= size[1]:
                maxheight = size[1]
                if force_fit:
                    maxwidth = size[0]
            else:
                break
        else:
            if force_fit:
                if (width >= size[0]) and (height >= size[1]):
                    maxwidth, maxheight = size
                else:
                    break
            else:
                if width >= size[0]:
                    maxwidth = size[0]
                if height >= size[1]:
                    maxheight = size[1]
    return maxwidth, maxheight