def get_size(file_path):
    """Return image size (width and height)."""
    try:
        im = _read_image(file_path)
    except (IOError, IndexError, TypeError, AttributeError) as e:
        logger = logging.getLogger(__name__)
        logger.error("Could not read size of %s due to %r", file_path, e)
    else:
        width, height = im.size
        return {
            'width': width,
            'height': height
        }