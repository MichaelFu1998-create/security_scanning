def imshow_flat(images, grid=None, showfun=None, bfill=1.0, bsz=(1,1), **opt):
    """
    imshow after applying flat_images
    :param images: [bhwc]
    :param grid: None for auto grid
    :param showfun: plt.imshow
    :param bfill: color for board fill
    :param bsz: size of board
    :param opt: option for showfun
    :return:
    """
    showfun = showfun or plt.imshow

    count = len(images)
    # decide grid shape if need pick one
    grid = grid or grid_recommend(count, ratio=sorted(images[0].shape[:2]))

    flatted = flat_images(images, grid, bfill=bfill, bsz=bsz)
    res = showfun(flatted, **opt)
    plt.draw()