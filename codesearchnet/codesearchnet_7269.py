def _timezone_format(value):
    """
    Generates a timezone aware datetime if the 'USE_TZ' setting is enabled

    :param value: The datetime value
    :return: A locale aware datetime
    """
    return timezone.make_aware(value, timezone.get_current_timezone()) if getattr(settings, 'USE_TZ', False) else value