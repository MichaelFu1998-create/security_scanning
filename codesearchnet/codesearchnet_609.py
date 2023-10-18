def keypoint_random_flip(
        image, annos, mask=None, prob=0.5, flip_list=(0, 1, 5, 6, 7, 2, 3, 4, 11, 12, 13, 8, 9, 10, 15, 14, 17, 16, 18)
):
    """Flip an image and corresponding keypoints.

    Parameters
    -----------
    image : 3 channel image
        The given image for augmentation.
    annos : list of list of floats
        The keypoints annotation of people.
    mask : single channel image or None
        The mask if available.
    prob : float, 0 to 1
        The probability to flip the image, if 1, always flip the image.
    flip_list : tuple of int
        Denotes how the keypoints number be changed after flipping which is required for pose estimation task.
        The left and right body should be maintained rather than switch.
        (Default COCO format).
        Set to an empty tuple if you don't need to maintain left and right information.

    Returns
    ----------
    preprocessed image, annos, mask

    """

    _prob = np.random.uniform(0, 1.0)
    if _prob < prob:
        return image, annos, mask

    _, width, _ = np.shape(image)
    image = cv2.flip(image, 1)
    mask = cv2.flip(mask, 1)
    new_joints = []
    for people in annos:  # TODO : speed up with affine transform
        new_keypoints = []
        for k in flip_list:
            point = people[k]
            if point[0] < 0 or point[1] < 0:
                new_keypoints.append((-1000, -1000))
                continue
            if point[0] > image.shape[1] - 1 or point[1] > image.shape[0] - 1:
                new_keypoints.append((-1000, -1000))
                continue
            if (width - point[0]) > image.shape[1] - 1:
                new_keypoints.append((-1000, -1000))
                continue
            new_keypoints.append((width - point[0], point[1]))
        new_joints.append(new_keypoints)
    annos = new_joints

    return image, annos, mask