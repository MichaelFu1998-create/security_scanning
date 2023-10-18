def rotate_crop(centerij, sz, angle, img=None, mode='constant', **kwargs):
    """
    rotate and crop
    if no img, then return crop function
    :param centerij:
    :param sz:
    :param angle:
    :param img: [h,w,d]
    :param mode: padding option
    :return: cropped image or function
    """
    # crop enough size ( 2 * sqrt(sum(sz^2) )
    # rotate
    from skimage import transform
    sz = np.array(sz)
    crop_half = int(np.ceil(np.sqrt(np.square(sz).sum())))

    if centerij[0] >= crop_half or centerij[1] >= crop_half:
        raise NotImplementedError

    slicei = slice(centerij[0] - crop_half, centerij[0] + crop_half)
    slicej = slice(centerij[1] - crop_half, centerij[1] + crop_half)

    # slicei = (centerij[0] - crop_half, centerij[0] + crop_half)
    # slicej = (centerij[1] - crop_half, centerij[1] + crop_half)

    # def _pad_if_need(im):
    #     imshape = im.shape
    #     pad_need = slicei[0] < 0 or slicej[0] < 0 or slice
    #     padwidth = [(slicei[0], np.maximum(0, slicei[1] - imshape[0])),
    #                 (slicej[0], np.maximum(0, slicej[1] - imshape[1]))]

    def _rotate_cropcenter(im):
        enoughcrop = im[slicei, slicej]

        rotated = transform.rotate(enoughcrop, angle, resize=False, preserve_range=True, mode=mode, **kwargs)
        return cropcenter(sz, rotated)
    if img is not None:
        return _rotate_cropcenter(img)

    return _rotate_cropcenter