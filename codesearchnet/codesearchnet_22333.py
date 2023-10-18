def _renderResource(resource, request):
    """
    Render a given resource.

    See `IResource.render <twisted:twisted.web.resource.IResource.render>`.
    """
    meth = getattr(resource, 'render_' + nativeString(request.method), None)
    if meth is None:
        try:
            allowedMethods = resource.allowedMethods
        except AttributeError:
            allowedMethods = _computeAllowedMethods(resource)
        raise UnsupportedMethod(allowedMethods)
    return meth(request)