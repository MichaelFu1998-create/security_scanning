def crop(img, center, sz, mode='constant'):
    """
    crop sz from ij as center
    :param img:
    :param center: ij
    :param sz:
    :param mode:
    :return:
    """
    center = np.array(center)
    sz = np.array(sz)
    istart = (center - sz / 2.).astype('int32')
    iend = istart + sz
    imsz = img.shape[:2]
    if np.any(istart < 0) or np.any(iend > imsz):
        # padding
        padwidth = [(np.minimum(0, istart[0]), np.maximum(0, iend[0]-imsz[0])),
                    (np.minimum(0, istart[1]), np.maximum(0, iend[1]-imsz[1]))]
        padwidth += [(0, 0)] * (len(img.shape) - 2)
        img = np.pad(img, padwidth, mode=mode)
        istart = (np.maximum(0, istart[0]), np.maximum(0, istart[1]))

        return img[istart[0]:istart[0]+sz[0], istart[1]:istart[1]+sz[1]]

    return img[istart[0]:iend[0], istart[1]:iend[1]]