def tiles_to_affine_shape(tiles):
    """
    Return Affine and shape of combined tiles.

    Parameters
    ----------
    tiles : iterable
        an iterable containing BufferedTiles

    Returns
    -------
    Affine, Shape
    """
    if not tiles:
        raise TypeError("no tiles provided")
    pixel_size = tiles[0].pixel_x_size
    left, bottom, right, top = (
        min([t.left for t in tiles]),
        min([t.bottom for t in tiles]),
        max([t.right for t in tiles]),
        max([t.top for t in tiles]),
    )
    return (
        Affine(pixel_size, 0, left, 0, -pixel_size, top),
        Shape(
            width=int(round((right - left) / pixel_size, 0)),
            height=int(round((top - bottom) / pixel_size, 0)),
        )
    )