def mark_read(user, message):
    """
    Mark message instance as read for user.
    Returns True if the message was `unread` and thus actually marked as `read` or False in case
    it is already `read` or it does not exist at all.

    :param user: user instance for the recipient
    :param message: a Message instance to mark as read
    """
    BackendClass = stored_messages_settings.STORAGE_BACKEND
    backend = BackendClass()
    backend.inbox_delete(user, message)