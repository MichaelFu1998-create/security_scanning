def serialize_options(opts):
    """
    A helper method to serialize and processes the options dictionary.
    """
    options = (opts or {}).copy()

    for key in opts.keys():
        if key not in DEFAULT_OPTIONS:
             LOG.warning("Unknown option passed to Flask-CORS: %s", key)

    # Ensure origins is a list of allowed origins with at least one entry.
    options['origins'] = sanitize_regex_param(options.get('origins'))
    options['allow_headers'] = sanitize_regex_param(options.get('allow_headers'))

    # This is expressly forbidden by the spec. Raise a value error so people
    # don't get burned in production.
    if r'.*' in options['origins'] and options['supports_credentials'] and options['send_wildcard']:
        raise ValueError("Cannot use supports_credentials in conjunction with"
                         "an origin string of '*'. See: "
                         "http://www.w3.org/TR/cors/#resource-requests")



    serialize_option(options, 'expose_headers')
    serialize_option(options, 'methods', upper=True)

    if isinstance(options.get('max_age'), timedelta):
        options['max_age'] = str(int(options['max_age'].total_seconds()))

    return options