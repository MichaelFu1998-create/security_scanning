def resource(**kwargs):
    """Wraps the decorated function in a lightweight resource."""
    def inner(function):
        name = kwargs.pop('name', None)
        if name is None:
            name = utils.dasherize(function.__name__)

        methods = kwargs.pop('methods', None)
        if isinstance(methods, six.string_types):
            # Tuple-ify the method if we got just a string.
            methods = methods,

        # Construct a handler.
        handler = (function, methods)

        if name not in _resources:
            # Initiate the handlers list.
            _handlers[name] = []

            # Construct a light-weight resource using the passed kwargs
            # as the arguments for the meta.
            from armet import resources
            kwargs['name'] = name

            class LightweightResource(resources.Resource):
                Meta = type(str('Meta'), (), kwargs)

                def route(self, request, response):
                    for handler, methods in _handlers[name]:
                        if methods is None or request.method in methods:
                            return handler(request, response)

                    resources.Resource.route(self)

            # Construct and add this resource.
            _resources[name] = LightweightResource

        # Add this to the handlers.
        _handlers[name].append(handler)

        # Return the resource.
        return _resources[name]

    # Return the inner method.
    return inner