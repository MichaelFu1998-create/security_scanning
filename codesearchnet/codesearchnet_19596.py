def _get_image_from_file(dir_path, image_file):
    """
    Get an instance of PIL.Image from the given file.
    @param {String} dir_path - The directory containing the image file
    @param {String} image_file - The filename of the image file within dir_path
    @return {PIL.Image} An instance of the image file as a PIL Image, or None
        if the functionality is not available. This could be because PIL is not
        present, or because it can't process the given file type.
    """
    # Save ourselves the effort if PIL is not present, and return None now
    if not PIL_ENABLED:
        return None
    # Put together full path
    path = os.path.join(dir_path, image_file)
    # Try to read the image
    img = None
    try:
        img = Image.open(path)
    except IOError as exptn:
        print('Error loading image file %s: %s' % (path, exptn))
    # Return image or None
    return img