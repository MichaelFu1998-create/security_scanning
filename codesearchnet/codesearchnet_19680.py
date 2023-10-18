def stored_messages_archive(context, num_elements=10):
    """
    Renders a list of archived messages for the current user
    """
    if "user" in context:
        user = context["user"]
        if user.is_authenticated():
            qs = MessageArchive.objects.select_related("message").filter(user=user)
            return {
                "messages": qs[:num_elements],
                "count": qs.count(),
            }