def event_choices(events):
    """ Get the possible events from settings """
    if events is None:
        msg = "Please add some events in settings.WEBHOOK_EVENTS."
        raise ImproperlyConfigured(msg)
    try:
        choices = [(x, x) for x in events]
    except TypeError:
        """ Not a valid iterator, so we raise an exception """
        msg = "settings.WEBHOOK_EVENTS must be an iterable object."
        raise ImproperlyConfigured(msg)
    return choices