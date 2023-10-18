def show_grid(images, rows=None, cols=None):
    """
    Converts the input images to a grid image and shows it in a new window.

    dtype support::

        minimum of (
            :func:`imgaug.imgaug.draw_grid`,
            :func:`imgaug.imgaug.imshow`
        )

    Parameters
    ----------
    images : (N,H,W,3) ndarray or iterable of (H,W,3) array
        See :func:`imgaug.draw_grid`.

    rows : None or int, optional
        See :func:`imgaug.draw_grid`.

    cols : None or int, optional
        See :func:`imgaug.draw_grid`.

    """
    grid = draw_grid(images, rows=rows, cols=cols)
    imshow(grid)