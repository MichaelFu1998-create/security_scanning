def add_message_for(users, level, message_text, extra_tags='', date=None, url=None, fail_silently=False):
    """
    Send a message to a list of users without passing through `django.contrib.messages`

    :param users: an iterable containing the recipients of the messages
    :param level: message level
    :param message_text: the string containing the message
    :param extra_tags: like the Django api, a string containing extra tags for the message
    :param date: a date, different than the default timezone.now
    :param url: an optional url
    :param fail_silently: not used at the moment
    """
    BackendClass = stored_messages_settings.STORAGE_BACKEND
    backend = BackendClass()
    m = backend.create_message(level, message_text, extra_tags, date, url)
    backend.archive_store(users, m)
    backend.inbox_store(users, m)