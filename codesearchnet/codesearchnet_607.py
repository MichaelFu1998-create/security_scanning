def keypoint_resize_random_crop(image, annos, mask=None, size=(368, 368)):
    """Reszie the image to make either its width or height equals to the given sizes.
    Then randomly crop image without influence scales.
    Resize the image match with the minimum size before cropping, this API will change the zoom scale of object.

    Parameters
    -----------
    image : 3 channel image
        The given image for augmentation.
    annos : list of list of floats
        The keypoints annotation of people.
    mask : single channel image or None
        The mask if available.
    size : tuple of int
        The size (height, width) of returned image.

    Returns
    ----------
    preprocessed image, annos, mask

    """

    if len(np.shape(image)) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    def resize_image(image, annos, mask, target_width, target_height):
        """Reszie image

        Parameters
        -----------
        image : 3 channel image
            The given image.
        annos : list of list of floats
            Keypoints of people
        mask : single channel image or None
            The mask if available.
        target_width : int
            Expected width of returned image.
        target_height : int
            Expected height of returned image.

        Returns
        ----------
        preprocessed input image, annos, mask

        """
        y, x, _ = np.shape(image)

        ratio_y = target_height / y
        ratio_x = target_width / x

        new_joints = []
        # update meta
        for people in annos:
            new_keypoints = []
            for keypoints in people:
                if keypoints[0] < 0 or keypoints[1] < 0:
                    new_keypoints.append((-1000, -1000))
                    continue
                pts = (int(keypoints[0] * ratio_x + 0.5), int(keypoints[1] * ratio_y + 0.5))
                if pts[0] > target_width - 1 or pts[1] > target_height - 1:
                    new_keypoints.append((-1000, -1000))
                    continue

                new_keypoints.append(pts)
            new_joints.append(new_keypoints)
        annos = new_joints

        new_image = cv2.resize(image, (target_width, target_height), interpolation=cv2.INTER_AREA)
        if mask is not None:
            new_mask = cv2.resize(mask, (target_width, target_height), interpolation=cv2.INTER_AREA)
            return new_image, annos, new_mask
        else:
            return new_image, annos, None

    _target_height = size[0]
    _target_width = size[1]
    if len(np.shape(image)) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    height, width, _ = np.shape(image)
    # print("the size of original img is:", height, width)
    if height <= width:
        ratio = _target_height / height
        new_width = int(ratio * width)
        if height == width:
            new_width = _target_height

        image, annos, mask = resize_image(image, annos, mask, new_width, _target_height)

        # for i in annos:
        #     if len(i) is not 19:
        #         print('Joints of person is not 19 ERROR FROM RESIZE')

        if new_width > _target_width:
            crop_range_x = np.random.randint(0, new_width - _target_width)
        else:
            crop_range_x = 0
        image = image[:, crop_range_x:crop_range_x + _target_width, :]
        if mask is not None:
            mask = mask[:, crop_range_x:crop_range_x + _target_width]
        # joint_list= []
        new_joints = []
        #annos-pepople-joints (must be 19 or [])
        for people in annos:
            # print("number of keypoints is", np.shape(people))
            new_keypoints = []
            for keypoints in people:
                if keypoints[0] < -10 or keypoints[1] < -10:
                    new_keypoints.append((-1000, -1000))
                    continue
                top = crop_range_x + _target_width - 1
                if keypoints[0] >= crop_range_x and keypoints[0] <= top:
                    # pts = (keypoints[0]-crop_range_x, keypoints[1])
                    pts = (int(keypoints[0] - crop_range_x), int(keypoints[1]))
                else:
                    pts = (-1000, -1000)
                new_keypoints.append(pts)

            new_joints.append(new_keypoints)
            # if len(new_keypoints) != 19:
            #     print('1:The Length of joints list should be 0 or 19 but actually:', len(new_keypoints))
        annos = new_joints

    if height > width:
        ratio = _target_width / width
        new_height = int(ratio * height)
        image, annos, mask = resize_image(image, annos, mask, _target_width, new_height)

        # for i in annos:
        #     if len(i) is not 19:
        #         print('Joints of person is not 19 ERROR')

        if new_height > _target_height:
            crop_range_y = np.random.randint(0, new_height - _target_height)

        else:
            crop_range_y = 0
        image = image[crop_range_y:crop_range_y + _target_width, :, :]
        if mask is not None:
            mask = mask[crop_range_y:crop_range_y + _target_width, :]
        new_joints = []

        for people in annos:  # TODO : speed up with affine transform
            new_keypoints = []
            for keypoints in people:

                # case orginal points are not usable
                if keypoints[0] < 0 or keypoints[1] < 0:
                    new_keypoints.append((-1000, -1000))
                    continue
                # y axis coordinate change
                bot = crop_range_y + _target_height - 1
                if keypoints[1] >= crop_range_y and keypoints[1] <= bot:
                    # pts = (keypoints[0], keypoints[1]-crop_range_y)
                    pts = (int(keypoints[0]), int(keypoints[1] - crop_range_y))
                    # if pts[0]>367 or pts[1]>367:
                    #     print('Error2')
                else:
                    pts = (-1000, -1000)

                new_keypoints.append(pts)

            new_joints.append(new_keypoints)
            # if len(new_keypoints) != 19:
            #     print('2:The Length of joints list should be 0 or 19 but actually:', len(new_keypoints))

        annos = new_joints

    # mask = cv2.resize(mask, (46, 46), interpolation=cv2.INTER_AREA)
    if mask is not None:
        return image, annos, mask
    else:
        return image, annos, None