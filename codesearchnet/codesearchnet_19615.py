def rand_brightness(imagez, scale=1.0, randfun=rand.normal(0., .1), clamp=(0., 1.)):
    """
    :param images:
    :param scale: scale for random value
    :param randfun: any randfun binding except shape
    :param clamp: clamping range
    :return:
    """
    l, h = clamp
    r = randfun((imagez[0].shape[0], 1, 1, 1)) * scale

    def apply(im):
        im += r
        im[im < l] = l
        im[im > h] = h
        return im

    return tuple(map(apply, imagez))