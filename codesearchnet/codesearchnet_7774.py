def process_video(filepath, outpath, settings):
    """Process a video: resize, create thumbnail."""

    logger = logging.getLogger(__name__)
    filename = os.path.split(filepath)[1]
    basename, ext = splitext(filename)

    try:
        if settings['use_orig'] and is_valid_html5_video(ext):
            outname = os.path.join(outpath, filename)
            utils.copy(filepath, outname, symlink=settings['orig_link'])
        else:
            valid_formats = ['mp4', 'webm']
            video_format = settings['video_format']

            if video_format not in valid_formats:
                logger.error('Invalid video_format. Please choose one of: %s',
                             valid_formats)
                raise ValueError

            outname = os.path.join(outpath, basename + '.' + video_format)
            generate_video(filepath, outname, settings,
                           options=settings.get(video_format + '_options'))
    except Exception:
        if logger.getEffectiveLevel() == logging.DEBUG:
            raise
        else:
            return Status.FAILURE

    if settings['make_thumbs']:
        thumb_name = os.path.join(outpath, get_thumb(settings, filename))
        try:
            generate_thumbnail(
                outname, thumb_name, settings['thumb_size'],
                settings['thumb_video_delay'], fit=settings['thumb_fit'],
                options=settings['jpg_options'],
                converter=settings['video_converter'])
        except Exception:
            if logger.getEffectiveLevel() == logging.DEBUG:
                raise
            else:
                return Status.FAILURE

    return Status.SUCCESS