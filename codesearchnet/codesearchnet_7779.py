def read_settings(filename=None):
    """Read settings from a config file in the source_dir root."""

    logger = logging.getLogger(__name__)
    logger.info("Reading settings ...")
    settings = _DEFAULT_CONFIG.copy()

    if filename:
        logger.debug("Settings file: %s", filename)
        settings_path = os.path.dirname(filename)
        tempdict = {}

        with open(filename) as f:
            code = compile(f.read(), filename, 'exec')
            exec(code, tempdict)

        settings.update((k, v) for k, v in tempdict.items()
                        if k not in ['__builtins__'])

        # Make the paths relative to the settings file
        paths = ['source', 'destination', 'watermark']

        if os.path.isdir(join(settings_path, settings['theme'])) and \
                os.path.isdir(join(settings_path, settings['theme'],
                                   'templates')):
            paths.append('theme')

        for p in paths:
            path = settings[p]
            if path and not isabs(path):
                settings[p] = abspath(normpath(join(settings_path, path)))
                logger.debug("Rewrite %s : %s -> %s", p, path, settings[p])

    for key in ('img_size', 'thumb_size', 'video_size'):
        w, h = settings[key]
        if h > w:
            settings[key] = (h, w)
            logger.warning("The %s setting should be specified with the "
                           "largest value first.", key)

    if not settings['img_processor']:
        logger.info('No Processor, images will not be resized')

    logger.debug('Settings:\n%s', pformat(settings, width=120))
    return settings