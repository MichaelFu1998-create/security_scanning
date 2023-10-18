def json_post_required(*decorator_args):
    """View decorator that enforces that the method was called using POST and
    contains a field containing a JSON dictionary. This method should
    only be used to wrap views and assumes the first argument of the method
    being wrapped is a ``request`` object.

    .. code-block:: python

        @json_post_required('data', 'json_data')
        def some_view(request):
            username = request.json_data['username']

    :param field:
        The name of the POST field that contains a JSON dictionary
    :param request_name:
        [optional] Name of the parameter on the request to put the
        deserialized JSON data. If not given the field name is used

    """
    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            field = decorator_args[0]
            if len(decorator_args) == 2:
                request_name = decorator_args[1]
            else:
                request_name = field

            request = args[0]
            if request.method != 'POST':
                logger.error('POST required for this url')
                raise Http404('only POST allowed for this url')

            if field not in request.POST:
                s = 'Expected field named %s in POST' % field
                logger.error(s)
                raise Http404(s)

            # deserialize the JSON and put it in the request
            setattr(request, request_name, json.loads(request.POST[field]))

            # everything verified, run the view
            return method(*args, **kwargs)
        return wrapper
    return decorator