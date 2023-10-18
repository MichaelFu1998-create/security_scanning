def keypoint_random_rotate(image, annos, mask=None, rg=15.):
    """Rotate an image and corresponding keypoints.

    Parameters
    -----------
    image : 3 channel image
        The given image for augmentation.
    annos : list of list of floats
        The keypoints annotation of people.
    mask : single channel image or None
        The mask if available.
    rg : int or float
        Degree to rotate, usually 0 ~ 180.

    Returns
    ----------
    preprocessed image, annos, mask

    """

    def _rotate_coord(shape, newxy, point, angle):
        angle = -1 * angle / 180.0 * math.pi
        ox, oy = shape
        px, py = point
        ox /= 2
        oy /= 2
        qx = math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        new_x, new_y = newxy
        qx += ox - new_x
        qy += oy - new_y
        return int(qx + 0.5), int(qy + 0.5)

    def _largest_rotated_rect(w, h, angle):
        """
        Get largest rectangle after rotation.
        http://stackoverflow.com/questions/16702966/rotate-image-and-crop-out-black-borders
        """
        angle = angle / 180.0 * math.pi
        if w <= 0 or h <= 0:
            return 0, 0

        width_is_longer = w >= h
        side_long, side_short = (w, h) if width_is_longer else (h, w)

        # since the solutions for angle, -angle and 180-angle are all the same,
        # if suffices to look at the first quadrant and the absolute values of sin,cos:
        sin_a, cos_a = abs(math.sin(angle)), abs(math.cos(angle))
        if side_short <= 2. * sin_a * cos_a * side_long:
            # half constrained case: two crop corners touch the longer side,
            #   the other two corners are on the mid-line parallel to the longer line
            x = 0.5 * side_short
            wr, hr = (x / sin_a, x / cos_a) if width_is_longer else (x / cos_a, x / sin_a)
        else:
            # fully constrained case: crop touches all 4 sides
            cos_2a = cos_a * cos_a - sin_a * sin_a
            wr, hr = (w * cos_a - h * sin_a) / cos_2a, (h * cos_a - w * sin_a) / cos_2a
        return int(np.round(wr)), int(np.round(hr))

    img_shape = np.shape(image)
    height = img_shape[0]
    width = img_shape[1]
    deg = np.random.uniform(-rg, rg)

    img = image
    center = (img.shape[1] * 0.5, img.shape[0] * 0.5)  # x, y
    rot_m = cv2.getRotationMatrix2D((int(center[0]), int(center[1])), deg, 1)
    ret = cv2.warpAffine(img, rot_m, img.shape[1::-1], flags=cv2.INTER_AREA, borderMode=cv2.BORDER_CONSTANT)
    if img.ndim == 3 and ret.ndim == 2:
        ret = ret[:, :, np.newaxis]
    neww, newh = _largest_rotated_rect(ret.shape[1], ret.shape[0], deg)
    neww = min(neww, ret.shape[1])
    newh = min(newh, ret.shape[0])
    newx = int(center[0] - neww * 0.5)
    newy = int(center[1] - newh * 0.5)
    # print(ret.shape, deg, newx, newy, neww, newh)
    img = ret[newy:newy + newh, newx:newx + neww]
    # adjust meta data
    adjust_joint_list = []
    for joint in annos:  # TODO : speed up with affine transform
        adjust_joint = []
        for point in joint:
            if point[0] < -100 or point[1] < -100:
                adjust_joint.append((-1000, -1000))
                continue

            x, y = _rotate_coord((width, height), (newx, newy), point, deg)

            if x > neww - 1 or y > newh - 1:
                adjust_joint.append((-1000, -1000))
                continue
            if x < 0 or y < 0:
                adjust_joint.append((-1000, -1000))
                continue

            adjust_joint.append((x, y))
        adjust_joint_list.append(adjust_joint)
    joint_list = adjust_joint_list

    if mask is not None:
        msk = mask
        center = (msk.shape[1] * 0.5, msk.shape[0] * 0.5)  # x, y
        rot_m = cv2.getRotationMatrix2D((int(center[0]), int(center[1])), deg, 1)
        ret = cv2.warpAffine(msk, rot_m, msk.shape[1::-1], flags=cv2.INTER_AREA, borderMode=cv2.BORDER_CONSTANT)
        if msk.ndim == 3 and msk.ndim == 2:
            ret = ret[:, :, np.newaxis]
        neww, newh = _largest_rotated_rect(ret.shape[1], ret.shape[0], deg)
        neww = min(neww, ret.shape[1])
        newh = min(newh, ret.shape[0])
        newx = int(center[0] - neww * 0.5)
        newy = int(center[1] - newh * 0.5)
        # print(ret.shape, deg, newx, newy, neww, newh)
        msk = ret[newy:newy + newh, newx:newx + neww]
        return img, joint_list, msk
    else:
        return img, joint_list, None