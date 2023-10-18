def keypoint_random_resize(image, annos, mask=None, zoom_range=(0.8, 1.2)):
    """Randomly resize an image and corresponding keypoints.
    The height and width of image will be changed independently, so the scale will be changed.

    Parameters
    -----------
    image : 3 channel image
        The given image for augmentation.
    annos : list of list of floats
        The keypoints annotation of people.
    mask : single channel image or None
        The mask if available.
    zoom_range : tuple of two floats
        The minimum and maximum factor to zoom in or out, e.g (0.5, 1) means zoom out 1~2 times.

    Returns
    ----------
    preprocessed image, annos, mask

    """
    height = image.shape[0]
    width = image.shape[1]
    _min, _max = zoom_range
    scalew = np.random.uniform(_min, _max)
    scaleh = np.random.uniform(_min, _max)

    neww = int(width * scalew)
    newh = int(height * scaleh)

    dst = cv2.resize(image, (neww, newh), interpolation=cv2.INTER_AREA)
    if mask is not None:
        mask = cv2.resize(mask, (neww, newh), interpolation=cv2.INTER_AREA)
    # adjust meta data
    adjust_joint_list = []
    for joint in annos:  # TODO : speed up with affine transform
        adjust_joint = []
        for point in joint:
            if point[0] < -100 or point[1] < -100:
                adjust_joint.append((-1000, -1000))
                continue
            adjust_joint.append((int(point[0] * scalew + 0.5), int(point[1] * scaleh + 0.5)))
        adjust_joint_list.append(adjust_joint)
    if mask is not None:
        return dst, adjust_joint_list, mask
    else:
        return dst, adjust_joint_list, None