def imslic(img, n_segments=100, aspect=None):
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
    from skimage.segmentation import (slic, mark_boundaries)
    from skimage.morphology import (dilation)

    if img.ndim == 2 or img.ndim == 3 and img.shape[-1] == 1:
        imz = np.stack([img, img, img], 2)
    else:
        imz = img

    slics = slic(imz, n_segments=n_segments)

    boundaries = mark_boundaries(imz, slics)
    return plt.imshow(boundaries, aspect=aspect)