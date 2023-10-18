def flat_images(images, grid=None, bfill=1.0, bsz=(1, 1)):
    """
    convert batch image to flat image with margin inserted
    [B,h,w,c] => [H,W,c]
    :param images:
    :param grid: patch grid cell size of (Row, Col)
    :param bfill: board filling value
    :param bsz: int or (int, int) board size
    :return: flatted image
    """
    if images.ndim == 4 and images.shape[-1] == 1:
        images = images.squeeze(axis=-1)

    grid = grid or grid_recommend(len(images), sorted(images[0].shape[:2]))
    if not isinstance(bsz, (tuple, list)):
        bsz = (bsz, bsz)

    # np.empty()
    imshape = list(images.shape)
    imshape[0] = grid[0] * grid[1]
    imshape[1] += bsz[0]
    imshape[2] += bsz[1]

    # data = np.empty((grid[0] * grid[1], imshape[1], imshape[2]), dtype=images.dtype)
    data = np.empty(imshape, dtype=images.dtype)

    data.fill(bfill)
    bslice0 = slice(0, -bsz[0]) if bsz[0] else slice(None, None)
    bslice1 = slice(0, -bsz[1]) if bsz[1] else slice(None, None)

    data[:len(images), bslice0, bslice1] = images

    imshape = list(grid) + imshape[1:]  # [grid[0], grid[1], H, W, [Channel]]
    data = data.reshape(imshape)
    if len(imshape) == 5:
        data = data.transpose(0, 2, 1, 3, 4)
        imshape = [imshape[0]*imshape[2], imshape[1]*imshape[3], imshape[4]]
    else:  # len == 4
        data = data.transpose(0, 2, 1, 3)
        imshape = [imshape[0]*imshape[2], imshape[1]*imshape[3]]
    data = data.reshape(imshape)

    # remove last margin
    data = data[bslice0, bslice1]

    return data