def get_exif_tags(data, datetime_format='%c'):
    """Make a simplified version with common tags from raw EXIF data."""

    logger = logging.getLogger(__name__)
    simple = {}

    for tag in ('Model', 'Make', 'LensModel'):
        if tag in data:
            if isinstance(data[tag], tuple):
                simple[tag] = data[tag][0].strip()
            else:
                simple[tag] = data[tag].strip()

    if 'FNumber' in data:
        fnumber = data['FNumber']
        try:
            simple['fstop'] = float(fnumber[0]) / fnumber[1]
        except Exception:
            logger.debug('Skipped invalid FNumber: %r', fnumber, exc_info=True)

    if 'FocalLength' in data:
        focal = data['FocalLength']
        try:
            simple['focal'] = round(float(focal[0]) / focal[1])
        except Exception:
            logger.debug('Skipped invalid FocalLength: %r', focal,
                         exc_info=True)

    if 'ExposureTime' in data:
        exptime = data['ExposureTime']
        if isinstance(exptime, tuple):
            try:
                simple['exposure'] = str(fractions.Fraction(exptime[0],
                                                            exptime[1]))
            except ZeroDivisionError:
                logger.info('Invalid ExposureTime: %r', exptime)
        elif isinstance(exptime, int):
            simple['exposure'] = str(exptime)
        else:
            logger.info('Unknown format for ExposureTime: %r', exptime)

    if data.get('ISOSpeedRatings'):
        simple['iso'] = data['ISOSpeedRatings']

    if 'DateTimeOriginal' in data:
        # Remove null bytes at the end if necessary
        date = data['DateTimeOriginal'].rsplit('\x00')[0]

        try:
            simple['dateobj'] = datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
            simple['datetime'] = simple['dateobj'].strftime(datetime_format)
        except (ValueError, TypeError) as e:
            logger.info('Could not parse DateTimeOriginal: %s', e)

    if 'GPSInfo' in data:
        info = data['GPSInfo']
        lat_info = info.get('GPSLatitude')
        lon_info = info.get('GPSLongitude')
        lat_ref_info = info.get('GPSLatitudeRef')
        lon_ref_info = info.get('GPSLongitudeRef')

        if lat_info and lon_info and lat_ref_info and lon_ref_info:
            try:
                lat = dms_to_degrees(lat_info)
                lon = dms_to_degrees(lon_info)
            except (ZeroDivisionError, ValueError, TypeError):
                logger.info('Failed to read GPS info')
            else:
                simple['gps'] = {
                    'lat': - lat if lat_ref_info != 'N' else lat,
                    'lon': - lon if lon_ref_info != 'E' else lon,
                }

    return simple