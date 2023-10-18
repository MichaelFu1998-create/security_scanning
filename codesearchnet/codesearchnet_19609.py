def rand_crop(sz, *imagez):
    """
    random crop
    # assume imagez has same size (H, W)
    # assume sz is less or equal than size of image
    :param sz: cropped image sz
    :param imagez: imagez
    :return: rand cropped image pairs or function bound to sz
    """

    def _rand_crop(*imgz):
        imsz = imgz[0].shape[:2]

        assert imsz[0] >= sz[0] and imsz[1] >= sz[1]

        si = np.random.randint(imsz[0] - sz[0]) if imsz[0] > sz[0] else 0
        sj = np.random.randint(imsz[1] - sz[1]) if imsz[1] > sz[1] else 0

        slicei = slice(si, si+sz[0])
        slicej = slice(sj, sj+sz[1])

        outs = tuple(img[slicei, slicej] for img in imgz)
        return tuple_or_not(*outs)

    return _rand_crop(*imagez) if imagez else _rand_crop