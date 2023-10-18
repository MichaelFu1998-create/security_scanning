def generate_image(source, outname, settings, options=None):
    """Image processor, rotate and resize the image.

    :param source: path to an image
    :param outname: output filename
    :param settings: settings dict
    :param options: dict with PIL options (quality, optimize, progressive)

    """

    logger = logging.getLogger(__name__)

    if settings['use_orig'] or source.endswith('.gif'):
        utils.copy(source, outname, symlink=settings['orig_link'])
        return

    img = _read_image(source)
    original_format = img.format

    if settings['copy_exif_data'] and settings['autorotate_images']:
        logger.warning("The 'autorotate_images' and 'copy_exif_data' settings "
                       "are not compatible because Sigal can't save the "
                       "modified Orientation tag.")

    # Preserve EXIF data
    if settings['copy_exif_data'] and _has_exif_tags(img):
        if options is not None:
            options = deepcopy(options)
        else:
            options = {}
        options['exif'] = img.info['exif']

    # Rotate the img, and catch IOError when PIL fails to read EXIF
    if settings['autorotate_images']:
        try:
            img = Transpose().process(img)
        except (IOError, IndexError):
            pass

    # Resize the image
    if settings['img_processor']:
        try:
            logger.debug('Processor: %s', settings['img_processor'])
            processor_cls = getattr(pilkit.processors,
                                    settings['img_processor'])
        except AttributeError:
            logger.error('Wrong processor name: %s', settings['img_processor'])
            sys.exit()

        width, height = settings['img_size']

        if img.size[0] < img.size[1]:
            # swap target size if image is in portrait mode
            height, width = width, height

        processor = processor_cls(width, height, upscale=False)
        img = processor.process(img)

    # signal.send() does not work here as plugins can modify the image, so we
    # iterate other the receivers to call them with the image.
    for receiver in signals.img_resized.receivers_for(img):
        img = receiver(img, settings=settings)

    outformat = img.format or original_format or 'JPEG'
    logger.debug('Save resized image to %s (%s)', outname, outformat)
    save_image(img, outname, outformat, options=options, autoconvert=True)