def draw_mpii_pose_to_image(image, poses, save_name='image.png'):
    """Draw people(s) into image using MPII dataset format as input, return or save the result image.

    This is an experimental API, can be changed in the future.

    Parameters
    -----------
    image : numpy.array
        The RGB image [height, width, channel].
    poses : list of dict
        The people(s) annotation in MPII format, see ``tl.files.load_mpii_pose_dataset``.
    save_name : None or str
        The name of image file (i.e. image.png), if None, not to save image.

    Returns
    --------
    numpy.array
        The saved image.

    Examples
    --------
    >>> import pprint
    >>> import tensorlayer as tl
    >>> img_train_list, ann_train_list, img_test_list, ann_test_list = tl.files.load_mpii_pose_dataset()
    >>> image = tl.vis.read_image(img_train_list[0])
    >>> tl.vis.draw_mpii_pose_to_image(image, ann_train_list[0], 'image.png')
    >>> pprint.pprint(ann_train_list[0])

    References
    -----------
    - `MPII Keyponts and ID <http://human-pose.mpi-inf.mpg.de/#download>`__
    """
    # import skimage
    # don't change the original image, and avoid error https://stackoverflow.com/questions/30249053/python-opencv-drawing-errors-after-manipulating-array-with-numpy
    image = image.copy()

    imh, imw = image.shape[0:2]
    thick = int((imh + imw) // 430)
    # radius = int(image.shape[1] / 500) + 1
    radius = int(thick * 1.5)

    if image.max() < 1:
        image = image * 255

    for people in poses:
        # Pose Keyponts
        joint_pos = people['joint_pos']
        # draw sketch
        # joint id (0 - r ankle, 1 - r knee, 2 - r hip, 3 - l hip, 4 - l knee,
        #           5 - l ankle, 6 - pelvis, 7 - thorax, 8 - upper neck,
        #           9 - head top, 10 - r wrist, 11 - r elbow, 12 - r shoulder,
        #           13 - l shoulder, 14 - l elbow, 15 - l wrist)
        #
        #               9
        #               8
        #         12 ** 7 ** 13
        #        *      *      *
        #       11      *       14
        #      *        *         *
        #     10    2 * 6 * 3     15
        #           *       *
        #           1       4
        #           *       *
        #           0       5

        lines = [
            [(0, 1), [100, 255, 100]],
            [(1, 2), [50, 255, 50]],
            [(2, 6), [0, 255, 0]],  # right leg
            [(3, 4), [100, 100, 255]],
            [(4, 5), [50, 50, 255]],
            [(6, 3), [0, 0, 255]],  # left leg
            [(6, 7), [255, 255, 100]],
            [(7, 8), [255, 150, 50]],  # body
            [(8, 9), [255, 200, 100]],  # head
            [(10, 11), [255, 100, 255]],
            [(11, 12), [255, 50, 255]],
            [(12, 8), [255, 0, 255]],  # right hand
            [(8, 13), [0, 255, 255]],
            [(13, 14), [100, 255, 255]],
            [(14, 15), [200, 255, 255]]  # left hand
        ]
        for line in lines:
            start, end = line[0]
            if (start in joint_pos) and (end in joint_pos):
                cv2.line(
                    image,
                    (int(joint_pos[start][0]), int(joint_pos[start][1])),
                    (int(joint_pos[end][0]), int(joint_pos[end][1])),  # up-left and botton-right
                    line[1],
                    thick
                )
                # rr, cc, val = skimage.draw.line_aa(int(joint_pos[start][1]), int(joint_pos[start][0]), int(joint_pos[end][1]), int(joint_pos[end][0]))
                # image[rr, cc] = line[1]
        # draw circles
        for pos in joint_pos.items():
            _, pos_loc = pos  # pos_id, pos_loc
            pos_loc = (int(pos_loc[0]), int(pos_loc[1]))
            cv2.circle(image, center=pos_loc, radius=radius, color=(200, 200, 200), thickness=-1)
            # rr, cc = skimage.draw.circle(int(pos_loc[1]), int(pos_loc[0]), radius)
            # image[rr, cc] = [0, 255, 0]

        # Head
        head_rect = people['head_rect']
        if head_rect:  # if head exists
            cv2.rectangle(
                image,
                (int(head_rect[0]), int(head_rect[1])),
                (int(head_rect[2]), int(head_rect[3])),  # up-left and botton-right
                [0, 180, 0],
                thick
            )

    if save_name is not None:
        # cv2.imwrite(save_name, image)
        save_image(image, save_name)
    return image