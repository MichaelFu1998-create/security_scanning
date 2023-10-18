def get_exif_data(filename):
    """Return a dict with the raw EXIF data."""

    logger = logging.getLogger(__name__)

    img = _read_image(filename)

    try:
        exif = img._getexif() or {}
    except ZeroDivisionError:
        logger.warning('Failed to read EXIF data.')
        return None

    data = {TAGS.get(tag, tag): value for tag, value in exif.items()}

    if 'GPSInfo' in data:
        try:
            data['GPSInfo'] = {GPSTAGS.get(tag, tag): value
                               for tag, value in data['GPSInfo'].items()}
        except AttributeError:
            logger = logging.getLogger(__name__)
            logger.info('Failed to get GPS Info')
            del data['GPSInfo']
    return data