def keypoint_random_crop(image, annos, mask=None, size=(368, 368)):
    """Randomly crop an image and corresponding keypoints without influence scales, given by ``keypoint_random_resize_shortestedge``.

    Parameters
    -----------
    image : 3 channel image
        The given image for augmentation.
    annos : list of list of floats
        The keypoints annotation of people.
    mask : single channel image or None
        The mask if available.
    size : tuple of int
        The size of returned image.

    Returns
    ----------
    preprocessed image, annotation, mask

    """

    _target_height = size[0]
    _target_width = size[1]
    target_size = (_target_width, _target_height)

    if len(np.shape(image)) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    height, width, _ = np.shape(image)

    for _ in range(50):
        x = random.randrange(0, width - target_size[0]) if width > target_size[0] else 0
        y = random.randrange(0, height - target_size[1]) if height > target_size[1] else 0

        # check whether any face is inside the box to generate a reasonably-balanced datasets
        for joint in annos:
            if x <= joint[0][0] < x + target_size[0] and y <= joint[0][1] < y + target_size[1]:
                break

    def pose_crop(image, annos, mask, x, y, w, h):  # TODO : speed up with affine transform
        # adjust image
        target_size = (w, h)

        img = image
        resized = img[y:y + target_size[1], x:x + target_size[0], :]
        resized_mask = mask[y:y + target_size[1], x:x + target_size[0]]
        # adjust meta data
        adjust_joint_list = []
        for joint in annos:
            adjust_joint = []
            for point in joint:
                if point[0] < -10 or point[1] < -10:
                    adjust_joint.append((-1000, -1000))
                    continue
                new_x, new_y = point[0] - x, point[1] - y
                # should not crop outside the image
                if new_x > w - 1 or new_y > h - 1:
                    adjust_joint.append((-1000, -1000))
                    continue
                adjust_joint.append((new_x, new_y))
            adjust_joint_list.append(adjust_joint)

        return resized, adjust_joint_list, resized_mask

    return pose_crop(image, annos, mask, x, y, target_size[0], target_size[1])