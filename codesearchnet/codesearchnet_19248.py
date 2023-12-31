def route(bp, *args, **kwargs):
    """Journey route decorator

    Enables simple serialization, deserialization and validation of Flask routes with the help of Marshmallow.

    :param bp: :class:`flask.Blueprint` object
    :param args: args to pass along to `Blueprint.route`
    :param kwargs:
        - :strict_slashes: Enable / disable strict slashes (default False)
        - :validate: Enable / disable body/query validation (default True)
        - :_query: Unmarshal Query string into this schema
        - :_body: Unmarshal JSON body into this schema
        - :marshal_with: Serialize the output with this schema
    :raises:
        - ValidationError if the query parameters or JSON body fails validation
    """

    kwargs['strict_slashes'] = kwargs.pop('strict_slashes', False)
    body = _validate_schema(kwargs.pop('_body', None))
    query = _validate_schema(kwargs.pop('_query', None))
    output = _validate_schema(kwargs.pop('marshal_with', None))
    validate = kwargs.pop('validate', True)

    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*inner_args, **inner_kwargs):
            """If a schema (_body and/or _query) was supplied to the route decorator, the deserialized
            :class`marshmallow.Schema` object is injected into the decorated function's kwargs."""

            try:
                if query is not None:
                    query.strict = validate
                    url = furl(request.url)
                    inner_kwargs['_query'] = query.load(data=url.args)

                if body is not None:
                    body.strict = validate
                    json_data = request.get_json()

                    if json_data is None:
                        # Set json_data to empty dict if body is empty, so it gets picked up by the validator
                        json_data = {}

                    inner_kwargs['_body'] = body.load(data=json_data)

            except ValidationError as err:
                return jsonify(err.messages), 422

            if output:
                data = output.dump(f(*inner_args, **inner_kwargs))
                return jsonify(data[0])

            return f(*inner_args, **inner_kwargs)

        return f

    return decorator