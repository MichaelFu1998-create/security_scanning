def blend_discrete(images, depthmask, depth=None):
    """
    depthmask : shape of [batch, h, w]
    """
    imshape = images.shape
    depth = depth or images.shape[3]
    blend = np.empty(shape=(imshape[0], imshape[1], imshape[2]))
    for d in range(depth):
        imask = (depthmask == d)
        channel = images[..., d]
        blend[imask] = channel[imask]
    return np.expand_dims(blend, axis=-1)