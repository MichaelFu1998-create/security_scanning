def imshow_grid(images, grid=None, showfun=None, **opt):
    """
    :param images: nhwc
    :return:
    """
    # assert images.ndim == 4  or list
    showfun = showfun or plt.imshow
    count = len(images)
    grid = grid or grid_recommend(count, sorted(images[0].shape[:2]))

    res = []
    for i, img in enumerate(images):
        # grid row first index
        plt.subplot2grid(grid, (i % grid[0], i // grid[0]))
        res.append(showfun(img.squeeze(), **opt))

    return res