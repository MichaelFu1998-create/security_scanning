def get_default_tag(app):
    '''Get the name of the view function used to prevent having to set the tag
    manually for every endpoint'''
    view_func = get_view_function(app, request.path, request.method)
    if view_func:
        return view_func.__name__