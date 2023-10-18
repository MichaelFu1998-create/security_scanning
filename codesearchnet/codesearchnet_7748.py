def generate_thumbnail(source, outname, box, fit=True, options=None,
                       thumb_fit_centering=(0.5, 0.5)):
    """Create a thumbnail image."""

    logger = logging.getLogger(__name__)
    img = _read_image(source)
    original_format = img.format

    if fit:
        img = ImageOps.fit(img, box, PILImage.ANTIALIAS,
                           centering=thumb_fit_centering)
    else:
        img.thumbnail(box, PILImage.ANTIALIAS)

    outformat = img.format or original_format or 'JPEG'
    logger.debug('Save thumnail image: %s (%s)', outname, outformat)
    save_image(img, outname, outformat, options=options, autoconvert=True)