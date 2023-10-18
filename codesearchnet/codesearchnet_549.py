def affine_transform_keypoints(coords_list, transform_matrix):
    """Transform keypoint coordinates according to a given affine transform matrix.
    OpenCV format, x is width.

    Note that, for pose estimation task, flipping requires maintaining the left and right body information.
    We should not flip the left and right body, so please use ``tl.prepro.keypoint_random_flip``.

    Parameters
    -----------
    coords_list : list of list of tuple/list
        The coordinates
        e.g., the keypoint coordinates of every person in an image.
    transform_matrix : numpy.array
        Transform matrix, OpenCV format.

    Examples
    ---------
    >>> # 1. get all affine transform matrices
    >>> M_rotate = tl.prepro.affine_rotation_matrix(angle=20)
    >>> M_flip = tl.prepro.affine_horizontal_flip_matrix(prob=1)
    >>> # 2. combine all affine transform matrices to one matrix
    >>> M_combined = dot(M_flip).dot(M_rotate)
    >>> # 3. transfrom the matrix from Cartesian coordinate (the origin in the middle of image)
    >>> # to Image coordinate (the origin on the top-left of image)
    >>> transform_matrix = tl.prepro.transform_matrix_offset_center(M_combined, x=w, y=h)
    >>> # 4. then we can transfrom the image once for all transformations
    >>> result = tl.prepro.affine_transform_cv2(image, transform_matrix)  # 76 times faster
    >>> # 5. transform keypoint coordinates
    >>> coords = [[(50, 100), (100, 100), (100, 50), (200, 200)], [(250, 50), (200, 50), (200, 100)]]
    >>> coords_result = tl.prepro.affine_transform_keypoints(coords, transform_matrix)
    """
    coords_result_list = []
    for coords in coords_list:
        coords = np.asarray(coords)
        coords = coords.transpose([1, 0])
        coords = np.insert(coords, 2, 1, axis=0)
        # print(coords)
        # print(transform_matrix)
        coords_result = np.matmul(transform_matrix, coords)
        coords_result = coords_result[0:2, :].transpose([1, 0])
        coords_result_list.append(coords_result)
    return coords_result_list