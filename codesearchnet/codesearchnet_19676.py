def mark_all_read(request):
    """
    Mark all messages as read (i.e. delete from inbox) for current logged in user
    """
    from .settings import stored_messages_settings
    backend = stored_messages_settings.STORAGE_BACKEND()
    backend.inbox_purge(request.user)
    return Response({"message": "All messages read"})