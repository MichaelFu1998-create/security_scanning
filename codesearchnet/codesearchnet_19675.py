def mark_all_read(user):
    """
    Mark all message instances for a user as read.

    :param user: user instance for the recipient
    """
    BackendClass = stored_messages_settings.STORAGE_BACKEND
    backend = BackendClass()
    backend.inbox_purge(user)