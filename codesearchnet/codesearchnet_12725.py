def convert(img, formats):
    """
        Convert the image to all the formats specified
    Parameters
    ----------
    img : PIL.Image.Image
        The image to convert
    formats : list
        List of all the formats to use
    Returns
    -------
    io.BytesIO
        A file object containing the converted image
    """
    media = None
    min_size = 0

    for kwargs in formats:
        f = io.BytesIO()
        if img.mode == "RGBA" and kwargs['format'] != "PNG":
            # convert to RGB if picture is too large as a png
            # this implies that the png format is the first in `formats`
            if min_size < 5 * 1024**2:
                continue
            else:
                img.convert('RGB')

        img.save(f, **kwargs)
        size = f.tell()

        if media is None or size < min_size:
            if media is not None:
                media.close()

            media = f
            min_size = size
        else:
            f.close()

    return media