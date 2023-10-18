def _get_src_from_image(img, fallback_image_file):
    """
    Get base-64 encoded data as a string for the given image. Fallback to return
    fallback_image_file if cannot get the image data or img is None.
    @param {Image} img - The PIL Image to get src data for
    @param {String} fallback_image_file - The filename of the image file,
        to be used when image data capture fails
    @return {String} The base-64 encoded image data string, or path to the file
        itself if not supported.
    """
    # If the image is None, then we can't process, so we should return the
    # path to the file itself
    if img is None:
        return fallback_image_file
    # Target format should be the same as the original image format, unless it's
    # a TIF/TIFF, which can't be displayed by most browsers; we convert these
    # to jpeg
    target_format = img.format
    if target_format.lower() in ['tif', 'tiff']:
        target_format = 'JPEG'
    # If we have an actual Image, great - put together the base64 image string
    try:
        bytesio = io.BytesIO()
        img.save(bytesio, target_format)
        byte_value = bytesio.getvalue()
        b64 = base64.b64encode(byte_value)
        return 'data:image/%s;base64,%s' % (target_format.lower(), b64)
    except IOError as exptn:
        print('IOError while saving image bytes: %s' % exptn)
        return fallback_image_file