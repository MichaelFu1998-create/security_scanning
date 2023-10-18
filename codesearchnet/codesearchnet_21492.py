def get_view_function(app, url, method):
    """Match a url and return the view and arguments
    it will be called with, or None if there is no view.
    Creds: http://stackoverflow.com/a/38488506
    """
    # pylint: disable=too-many-return-statements

    adapter = app.create_url_adapter(request)

    try:
        match = adapter.match(url, method=method)
    except RequestRedirect as ex:
        # recursively match redirects
        return get_view_function(app, ex.new_url, method)
    except (MethodNotAllowed, NotFound):
        # no match
        return None

    try:
        return app.view_functions[match[0]]
    except KeyError:
        # no view is associated with the endpoint
        return None