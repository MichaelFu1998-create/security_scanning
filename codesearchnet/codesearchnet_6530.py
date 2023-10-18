def filterchain_all(request, app, model, field, foreign_key_app_name,
                    foreign_key_model_name, foreign_key_field_name, value):
    """Returns filtered results followed by excluded results below."""
    model_class = get_model(app, model)
    keywords = get_keywords(field, value)

    # SECURITY: Make sure all smart selects requests are opt-in
    foreign_model_class = get_model(foreign_key_app_name, foreign_key_model_name)
    if not any([(isinstance(f, ChainedManyToManyField) or
                 isinstance(f, ChainedForeignKey))
                for f in foreign_model_class._meta.get_fields()]):
        raise PermissionDenied("Smart select disallowed")

    # filter queryset using limit_choices_to
    limit_choices_to = get_limit_choices_to(foreign_key_app_name, foreign_key_model_name, foreign_key_field_name)
    queryset = get_queryset(model_class, limit_choices_to=limit_choices_to)

    filtered = list(do_filter(queryset, keywords))
    # Sort results if model doesn't include a default ordering.
    if not getattr(model_class._meta, 'ordering', False):
        sort_results(list(filtered))

    excluded = list(do_filter(queryset, keywords, exclude=True))
    # Sort results if model doesn't include a default ordering.
    if not getattr(model_class._meta, 'ordering', False):
        sort_results(list(excluded))

    # Empty choice to separate filtered and excluded results.
    empty_choice = {'value': "", 'display': "---------"}

    serialized_results = (
        serialize_results(filtered) +
        [empty_choice] +
        serialize_results(excluded)
    )

    return JsonResponse(serialized_results, safe=False)