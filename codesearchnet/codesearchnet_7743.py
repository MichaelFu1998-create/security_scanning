def build(source, destination, debug, verbose, force, config, theme, title,
          ncpu):
    """Run sigal to process a directory.

    If provided, 'source', 'destination' and 'theme' will override the
    corresponding values from the settings file.

    """
    level = ((debug and logging.DEBUG) or (verbose and logging.INFO) or
             logging.WARNING)
    init_logging(__name__, level=level)
    logger = logging.getLogger(__name__)

    if not os.path.isfile(config):
        logger.error("Settings file not found: %s", config)
        sys.exit(1)

    start_time = time.time()
    settings = read_settings(config)

    for key in ('source', 'destination', 'theme'):
        arg = locals()[key]
        if arg is not None:
            settings[key] = os.path.abspath(arg)
        logger.info("%12s : %s", key.capitalize(), settings[key])

    if not settings['source'] or not os.path.isdir(settings['source']):
        logger.error("Input directory not found: %s", settings['source'])
        sys.exit(1)

    # on windows os.path.relpath raises a ValueError if the two paths are on
    # different drives, in that case we just ignore the exception as the two
    # paths are anyway not relative
    relative_check = True
    try:
        relative_check = os.path.relpath(settings['destination'],
                                         settings['source']).startswith('..')
    except ValueError:
        pass

    if not relative_check:
        logger.error("Output directory should be outside of the input "
                     "directory.")
        sys.exit(1)

    if title:
        settings['title'] = title

    locale.setlocale(locale.LC_ALL, settings['locale'])
    init_plugins(settings)

    gal = Gallery(settings, ncpu=ncpu)
    gal.build(force=force)

    # copy extra files
    for src, dst in settings['files_to_copy']:
        src = os.path.join(settings['source'], src)
        dst = os.path.join(settings['destination'], dst)
        logger.debug('Copy %s to %s', src, dst)
        copy(src, dst, symlink=settings['orig_link'], rellink=settings['rel_link'])

    stats = gal.stats

    def format_stats(_type):
        opt = ["{} {}".format(stats[_type + '_' + subtype], subtype)
               for subtype in ('skipped', 'failed')
               if stats[_type + '_' + subtype] > 0]
        opt = ' ({})'.format(', '.join(opt)) if opt else ''
        return '{} {}s{}'.format(stats[_type], _type, opt)

    print('Done.\nProcessed {} and {} in {:.2f} seconds.'
          .format(format_stats('image'), format_stats('video'),
                  time.time() - start_time))