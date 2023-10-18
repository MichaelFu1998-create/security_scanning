def _filter_kwargs_to_query_params(filter_kwargs):
    """
    Convert API keyword args to a mapping of URL query parameters.  Except for
    "added_after", all keywords are mapped to match filters, i.e. to a query
    parameter of the form "match[<kwarg>]".  "added_after" is left alone, since
    it's a special filter, as defined in the spec.

    Each value can be a single value or iterable of values.  "version" and
    "added_after" get special treatment, since they are timestamp-valued:
    datetime.datetime instances are supported and automatically converted to
    STIX-compliant strings.  Other than that, all values must be strings.  None
    values, empty lists, etc are silently ignored.

    Args:
        filter_kwargs: The filter information, as a mapping.

    Returns:
        query_params (dict): The query parameter map, mapping strings to
            strings.

    """
    query_params = {}
    for kwarg, arglist in six.iteritems(filter_kwargs):
        # If user passes an empty list, None, etc, silently skip?
        if not arglist:
            continue

        # force iterability, for the sake of code uniformity
        if not hasattr(arglist, "__iter__") or \
                isinstance(arglist, six.string_types):
            arglist = arglist,

        if kwarg == "version":
            query_params["match[version]"] = ",".join(
                _ensure_datetime_to_string(val) for val in arglist
            )

        elif kwarg == "added_after":
            if len(arglist) > 1:
                raise InvalidArgumentsError("No more than one value for filter"
                                            " 'added_after' may be given")

            query_params["added_after"] = ",".join(
                _ensure_datetime_to_string(val) for val in arglist
            )

        else:
            query_params["match[" + kwarg + "]"] = ",".join(arglist)

    return query_params