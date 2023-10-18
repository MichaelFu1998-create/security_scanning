def imslic2(img, n_segments=100, color=None, outline_color=None, mode='thick', **kwargs):
    """
    slic args :
    n_segments=100, compactness=10., max_iter=10,
    sigma=0, spacing=None,
    multichannel=True, convert2lab=None, enforce_connectivity=True,
    min_size_factor=0.5, max_size_factor=3, slic_zero=False

    mark_boundaries args:
    label_img, color=(1, 1, 0), outline_color=None, mode='outer', background_label=0

    imshow args:
    cmap=None, norm=None, aspect=None, interpolation=None,
    alpha=None, vmin=None, vmax=None, origin=None,
    extent=None, shape=None, filternorm=1, filterrad=4.0,
    imlim=None, resample=None, url=None, hold=None, data=None,

    :param img:
    :param slicarg:
    :param slickw:
    :return:
    """
    from skimage.segmentation import (slic, find_boundaries) # mark_boundaries
    from skimage.morphology import (dilation)

    kwslic = {'compactness', 'max_iter', 'sigma', 'spacing', 'multichannel', 'convert2lab',
              'enforce_connectivity', 'min_size_factor', 'max_size_factor', 'slic_zero=False'}
    imshowkw = {'cmap', 'norm', 'aspect', 'interpolation', 'alpha', 'vmin', 'vmax', 'origin',
                'extent', 'shape', 'filternorm', 'filterrad', 'imlim', 'resample', 'url', 'hold', 'data'}

    slicarg = {k: v for k, v in kwargs.iteritems() if k in kwslic}
    imshowarg = {k: v for k, v in kwargs.iteritems() if k in imshowkw}

    if img.ndim == 2 or img.ndim == 3 and img.shape[-1] == 1:
        imz = np.stack([img, img, img], 2)
        color = color or 1.
    else:
        imgz = img
        color = color or (1,1,0)

    slics = slic(imz, n_segments=n_segments, **slicarg)

    boundaries = find_boundaries(slics, mode=mode)
    if outline_color is not None:
        outlines = dilation(boundaries, np.ones((3, 3), np.uint8))
        img[outlines] = outline_color
    img[boundaries] = color
    return plt.imshow(img, **imshowarg)