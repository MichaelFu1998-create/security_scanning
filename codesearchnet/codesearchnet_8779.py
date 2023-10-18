def validate_image_size(image):
    """
    Validate that a particular image size.
    """
    config = get_app_config()
    valid_max_image_size_in_bytes = config.valid_max_image_size * 1024
    if config and not image.size <= valid_max_image_size_in_bytes:
        raise ValidationError(
            _("The logo image file size must be less than or equal to %s KB.") % config.valid_max_image_size)