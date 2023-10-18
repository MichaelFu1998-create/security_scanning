def _crop_img_to(image, slices, copy=True):
    """Crops image to a smaller size

    Crop img to size indicated by slices and modify the affine accordingly.

    Parameters
    ----------
    image: img-like object or str
        Can either be:
        - a file path to a Nifti image
        - any object with get_data() and get_affine() methods, e.g., nibabel.Nifti1Image.
        If niimg is a string, consider it as a path to Nifti image and
        call nibabel.load on it. If it is an object, check if get_data()
        and get_affine() methods are present, raise TypeError otherwise.

        Image to be cropped.

    slices: list of slices
        Defines the range of the crop.
        E.g. [slice(20, 200), slice(40, 150), slice(0, 100)]
        defines a 3D cube

        If slices has less entries than image has dimensions,
        the slices will be applied to the first len(slices) dimensions.

    copy: boolean
        Specifies whether cropped data is to be copied or not.
        Default: True

    Returns
    -------
    cropped_img: img-like object
        Cropped version of the input image
    """

    img    = check_img(image)
    data   = img.get_data()
    affine = img.get_affine()

    cropped_data = data[slices]
    if copy:
        cropped_data   = cropped_data.copy()

    linear_part        = affine[:3, :3]
    old_origin         = affine[:3,  3]
    new_origin_voxel   = np.array([s.start for s in slices])
    new_origin         = old_origin + linear_part.dot(new_origin_voxel)

    new_affine         = np.eye(4)
    new_affine[:3, :3] = linear_part
    new_affine[:3,  3] = new_origin

    new_img = nib.Nifti1Image(cropped_data, new_affine)

    return new_img