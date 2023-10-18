def validate_image_extension(value):
    """
    Validate that a particular image extension.
    """
    config = get_app_config()
    ext = os.path.splitext(value.name)[1]
    if config and not ext.lower() in config.valid_image_extensions:
        raise ValidationError(_("Unsupported file extension."))