def get_data(img):
    """Get the data in the image without having a side effect on the Nifti1Image object

    Parameters
    ----------
    img: Nifti1Image

    Returns
    -------
    np.ndarray
    """
    if hasattr(img, '_data_cache') and img._data_cache is None:
        # Copy locally the nifti_image to avoid the side effect of data
        # loading
        img = copy.deepcopy(img)
    # force garbage collector
    gc.collect()
    return img.get_data()