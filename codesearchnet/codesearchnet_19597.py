def _get_image_link_target_from_file(dir_path, image_file, force_no_processing=False):
    """
    Get the value to be used as the href for links from thumbnail images. For
    most image formats this will simply be the image file name itself. However,
    some image formats (tif) are not natively displayable by many browsers and
    therefore we must link to image data in another format.
    @param {String} dir_path - The directory containing the image file
    @param {String} image_file - The filename of the image file within dir_path
    @param {Boolean=False} force_no_processing - If True, do not attempt to
        actually process a thumbnail, PIL image or anything. Simply return the
        image filename as src.
    @return {String} The href to use.
    """
    # If we've specified to force no processing, just return the image filename
    if force_no_processing:
        return image_file
    # First try to get an image
    img = _get_image_from_file(dir_path, image_file)
    # If format is directly displayable in-browser, just return the filename
    # Else, we need to return a full-sized chunk of displayable image data
    if img.format.lower() in ['tif', 'tiff']:
        return _get_image_src_from_file(
            dir_path, image_file, force_no_processing
        )
    return image_file