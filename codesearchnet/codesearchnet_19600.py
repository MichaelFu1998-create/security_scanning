def _get_thumbnail_image_from_file(dir_path, image_file):
    """
    Get a PIL.Image from the given image file which has been scaled down to
    THUMBNAIL_WIDTH wide.
    @param {String} dir_path - The directory containing the image file
    @param {String} image_file - The filename of the image file within dir_path
    @return {PIL.Image} An instance of the thumbnail as a PIL Image, or None
        if the functionality is not available. See _get_image_from_file for
        details.
    """
    # Get image
    img = _get_image_from_file(dir_path, image_file)
    # If it's not supported, exit now
    if img is None:
        return None
    if img.format.lower() == 'gif':
        return None
    # Get image dimensions
    img_width, img_height = img.size
    # We need to perform a resize - first, work out the scale ratio to take the
    # image width to THUMBNAIL_WIDTH (THUMBNAIL_WIDTH:img_width ratio)
    scale_ratio = THUMBNAIL_WIDTH / float(img_width)
    # Work out target image height based on the scale ratio
    target_height = int(scale_ratio * img_height)
    # Perform the resize
    try:
        img.thumbnail((THUMBNAIL_WIDTH, target_height), resample=RESAMPLE)
    except IOError as exptn:
        print('WARNING: IOError when thumbnailing %s/%s: %s' % (
            dir_path, image_file, exptn
        ))
        return None
    # Return the resized image
    return img