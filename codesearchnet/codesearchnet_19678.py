def stored_messages_list(context, num_elements=10):
    """
    Renders a list of unread stored messages for the current user
    """
    if "user" in context:
        user = context["user"]
        if user.is_authenticated():
            qs = Inbox.objects.select_related("message").filter(user=user)
            return {
                "messages": qs[:num_elements],
                "count": qs.count(),
            }