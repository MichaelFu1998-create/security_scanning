def pad_if_need(sz_atleast, img, mode='constant'):
    # fixme : function or ....
    """
    pad img if need to guarantee minumum size
    :param sz_atleast: [H,W] at least
    :param img: image np.array [H,W, ...]
    :param mode: str, padding mode
    :return: padded image or asis if enought size
    """
    # sz_atleast = np.asarray(sz_atleast)
    imsz = img.shape[:2]  # assume img [H,W, ...]
    padneed = np.asarray((sz_atleast[0] - imsz[0], sz_atleast[1] - imsz[1]))
    if np.any(padneed > 0):
        # need padding
        padding = np.zeros((img.ndim, 2), dtype='int16')
        padneed = np.maximum(padneed, 0)
        padding[:2, 0] = padneed/2
        padding[:2, 1] = padneed - padneed/2
        img = np.pad(img, padding, mode=mode)

    return img