def example4():
    """ Example 4: Transforming coordinates using affine matrix. """
    transform_matrix = create_transformation_matrix()
    result = tl.prepro.affine_transform_cv2(image, transform_matrix)  # 76 times faster
    # Transform keypoint coordinates
    coords = [[(50, 100), (100, 100), (100, 50), (200, 200)], [(250, 50), (200, 50), (200, 100)]]
    coords_result = tl.prepro.affine_transform_keypoints(coords, transform_matrix)

    def imwrite(image, coords_list, name):
        coords_list_ = []
        for coords in coords_list:
            coords = np.array(coords, np.int32)
            coords = coords.reshape((-1, 1, 2))
            coords_list_.append(coords)
        image = cv2.polylines(image, coords_list_, True, (0, 255, 255), 3)
        cv2.imwrite(name, image[..., ::-1])

    imwrite(image, coords, '_with_keypoints_origin.png')
    imwrite(result, coords_result, '_with_keypoints_result.png')