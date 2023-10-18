def cropcenter(sz, img=None):
    """
    if no img, then return crop function
    :param sz:
    :param img:
    :return:
    """
    l = len(sz)
    sz = np.array(sz)

    def wrapped(im):
        imsz = np.array(im.shape)
        s = (imsz[:l] - sz) / 2  # start index
        to = s + sz  # end index

        # img[s[0]:to[0], ... s[end]:to[end], ...]
        slices = [slice(s, e) for s, e in zip(s, to)]

        return im[slices]

    if img is not None:
        return wrapped(img)

    return wrapped