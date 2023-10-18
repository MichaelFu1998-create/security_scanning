def _get_thumbnail_src_from_file(dir_path, image_file, force_no_processing=False):
    """
    Get base-64 encoded data as a string for the given image file's thumbnail,
    for use directly in HTML <img> tags, or a path to the original if image
    scaling is not supported.
    @param {String} dir_path - The directory containing the image file
    @param {String} image_file - The filename of the image file within dir_path
    @param {Boolean=False} force_no_processing - If True, do not attempt to
        actually process a thumbnail, PIL image or anything. Simply return the
        image filename as src.
    @return {String} The base-64 encoded image data string, or path to the file
        itself if not supported.
    """
    # If we've specified to force no processing, just return the image filename
    if force_no_processing:
        if image_file.endswith('tif') or image_file.endswith('tiff'):
            return UNSUPPORTED_IMAGE_TYPE_DATA
        return image_file
    # First try to get a thumbnail image
    img = _get_thumbnail_image_from_file(dir_path, image_file)
    return _get_src_from_image(img, image_file)