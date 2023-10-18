def stored_messages_count(context):
    """
    Renders a list of unread stored messages for the current user
    """
    if "user" in context:
        user = context["user"]
        if user.is_authenticated():
            return Inbox.objects.select_related("message").filter(user=user).count()