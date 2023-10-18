def broadcast_message(level, message_text, extra_tags='', date=None, url=None, fail_silently=False):
    """
    Send a message to all users aka broadcast.

    :param level: message level
    :param message_text: the string containing the message
    :param extra_tags: like the Django api, a string containing extra tags for the message
    :param date: a date, different than the default timezone.now
    :param url: an optional url
    :param fail_silently: not used at the moment
    """
    from django.contrib.auth import get_user_model
    users = get_user_model().objects.all()
    add_message_for(users, level, message_text, extra_tags=extra_tags, date=date, url=url, fail_silently=fail_silently)