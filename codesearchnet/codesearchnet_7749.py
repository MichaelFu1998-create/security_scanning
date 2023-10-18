def process_image(filepath, outpath, settings):
    """Process one image: resize, create thumbnail."""

    logger = logging.getLogger(__name__)
    logger.info('Processing %s', filepath)
    filename = os.path.split(filepath)[1]
    outname = os.path.join(outpath, filename)
    ext = os.path.splitext(filename)[1]

    if ext in ('.jpg', '.jpeg', '.JPG', '.JPEG'):
        options = settings['jpg_options']
    elif ext == '.png':
        options = {'optimize': True}
    else:
        options = {}

    try:
        generate_image(filepath, outname, settings, options=options)

        if settings['make_thumbs']:
            thumb_name = os.path.join(outpath, get_thumb(settings, filename))
            generate_thumbnail(
                outname, thumb_name, settings['thumb_size'],
                fit=settings['thumb_fit'], options=options,
                thumb_fit_centering=settings["thumb_fit_centering"])
    except Exception as e:
        logger.info('Failed to process: %r', e)
        if logger.getEffectiveLevel() == logging.DEBUG:
            raise
        else:
            return Status.FAILURE

    return Status.SUCCESS