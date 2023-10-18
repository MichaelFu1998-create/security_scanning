def messages_from_response(response):
    """Returns a list of the messages from the django MessageMiddleware
    package contained within the given response.  This is to be used during
    unit testing when trying to see if a message was set properly in a view.

    :param response: HttpResponse object, likely obtained through a
        test client.get() or client.post() call

    :returns: a list of tuples (message_string, message_level), one for each
        message in the response context
    """
    messages = []
    if hasattr(response, 'context') and response.context and \
            'messages' in response.context:
        messages = response.context['messages']
    elif hasattr(response, 'cookies'):
        # no "context" set-up or no messages item, check for message info in
        # the cookies
        morsel = response.cookies.get('messages')
        if not morsel:
            return []

        # use the decoder in the CookieStore to process and get a list of
        # messages
        from django.contrib.messages.storage.cookie import CookieStorage
        store = CookieStorage(FakeRequest())
        messages = store._decode(morsel.value)
    else:
        return []

    return [(m.message, m.level) for m in messages]