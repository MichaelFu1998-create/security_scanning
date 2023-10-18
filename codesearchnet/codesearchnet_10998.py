def available_templates(value):
    """Scan for available templates in effect_templates"""
    templates = list_templates()

    if value not in templates:
        raise ArgumentTypeError("Effect template '{}' does not exist.\n Available templates: {} ".format(
            value, ", ".join(templates)))

    return value