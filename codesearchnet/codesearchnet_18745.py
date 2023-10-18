def mock_request():
    """
    Generate a fake request object to allow oEmbeds to use context processors.
    """
    current_site = Site.objects.get_current()
    request = HttpRequest()
    request.META['SERVER_NAME'] = current_site.domain
    return request