def validate_params(required, optional, params):
    """
    Helps us validate the parameters for the request

    :param valid_options: a list of strings of valid options for the
                          api request
    :param params: a dict, the key-value store which we really only care about
                   the key which has tells us what the user is using for the
                   API request

    :returns: None or throws an exception if the validation fails
    """

    missing_fields = [x for x in required if x not in params]
    if missing_fields:
        field_strings = ", ".join(missing_fields)
        raise Exception("Missing fields: %s" % field_strings)

    disallowed_fields = [x for x in params if x not in optional and x not in required]
    if disallowed_fields:
        field_strings = ", ".join(disallowed_fields)
        raise Exception("Disallowed fields: %s" % field_strings)