def do_filter(qs, keywords, exclude=False):
    """
    Filter queryset based on keywords.
    Support for multiple-selected parent values.
    """
    and_q = Q()
    for keyword, value in iteritems(keywords):
        try:
            values = value.split(",")
            if len(values) > 0:
                or_q = Q()
                for value in values:
                    or_q |= Q(**{keyword: value})
                and_q &= or_q
        except AttributeError:
            # value can be a bool
            and_q &= Q(**{keyword: value})
    if exclude:
        qs = qs.exclude(and_q)
    else:
        qs = qs.filter(and_q)
    return qs