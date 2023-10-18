def elastic_transform(im, alpha=0.5, sigma=0.2, affine_sigma=1.):
    """
    Based on https://gist.github.com/erniejunior/601cdf56d2b424757de5
    elastic deformation of images as described in [Simard2003]
    """
    # fixme : not implemented for multi channel !
    import cv2

    islist = isinstance(im, (tuple, list))
    ima = im[0] if islist else im

    # image shape
    shape = ima.shape
    shape_size = shape[:2]

    # Random affine transform
    center_square = np.float32(shape_size) // 2
    square_size = min(shape_size) // 3
    pts1 = np.float32([center_square + square_size,
                       [center_square[0] + square_size, center_square[1] - square_size],
                       center_square - square_size])
    pts2 = pts1 + np.random.uniform(-affine_sigma, affine_sigma, size=pts1.shape).astype(np.float32)
    M = cv2.getAffineTransform(pts1, pts2)
    if islist:
        res = []
        for i, ima in enumerate(im):
            if i == 0:
                res.append(cv2.warpAffine(ima, M, shape_size[::-1], borderMode=cv2.BORDER_REFLECT_101))
            else:
                res.append(cv2.warpAffine(ima, M, shape_size[::-1]))
        im = res
    else:
        ima = cv2.warpAffine(ima, M, shape_size[::-1], borderMode=cv2.BORDER_REFLECT_101)
        # ima = cv2.warpAffine(ima, M, shape_size[::-1])

    # fast gaussian filter
    blur_size = int(4 * sigma) | 1
    dx = cv2.GaussianBlur((np.random.rand(*shape) * 2 - 1), ksize=(blur_size, blur_size), sigmaX=sigma) * alpha
    dy = cv2.GaussianBlur((np.random.rand(*shape) * 2 - 1), ksize=(blur_size, blur_size), sigmaX=sigma) * alpha

    # remap
    x, y = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]))
    map_x, map_y = (y + dy).astype('float32'), (x + dx).astype('float32')

    def remap(data):
        r = cv2.remap(data, map_y, map_x, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
        return r[..., np.newaxis]

    if islist:
        return tuple([remap(ima) for ima in im])
    else:
        return remap(ima)