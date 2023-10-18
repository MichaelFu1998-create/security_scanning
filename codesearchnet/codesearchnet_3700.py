def jt_aggregate(func, is_create=False, has_pk=False):
    """Decorator to aggregate unified_jt-related fields.

    Args:
        func: The CURD method to be decorated.
        is_create: Boolean flag showing whether this method is create.
        has_pk: Boolean flag showing whether this method uses pk as argument.

    Returns:
        A function with necessary click-related attributes whose keyworded
        arguments are aggregated.

    Raises:
        exc.UsageError: Either more than one unified jt fields are
            provided, or none is provided when is_create flag is set.
    """
    def helper(kwargs, obj):
        """The helper function preceding actual function that aggregates
        unified jt fields.
        """
        unified_job_template = None
        for item in UNIFIED_JT:
            if kwargs.get(item, None) is not None:
                jt_id = kwargs.pop(item)
                if unified_job_template is None:
                    unified_job_template = (item, jt_id)
                else:
                    raise exc.UsageError(
                        'More than one unified job template fields provided, '
                        'please tighten your criteria.'
                    )
        if unified_job_template is not None:
            kwargs['unified_job_template'] = unified_job_template[1]
            obj.identity = tuple(list(obj.identity) + ['unified_job_template'])
            return '/'.join([UNIFIED_JT[unified_job_template[0]],
                             str(unified_job_template[1]), 'schedules/'])
        elif is_create:
            raise exc.UsageError('You must provide exactly one unified job'
                                 ' template field during creation.')

    def decorator_without_pk(obj, *args, **kwargs):
        old_endpoint = obj.endpoint
        new_endpoint = helper(kwargs, obj)
        if is_create:
            obj.endpoint = new_endpoint
        result = func(obj, *args, **kwargs)
        obj.endpoint = old_endpoint
        return result

    def decorator_with_pk(obj, pk=None, *args, **kwargs):
        old_endpoint = obj.endpoint
        new_endpoint = helper(kwargs, obj)
        if is_create:
            obj.endpoint = new_endpoint
        result = func(obj, pk=pk, *args, **kwargs)
        obj.endpoint = old_endpoint
        return result

    decorator = decorator_with_pk if has_pk else decorator_without_pk
    for item in CLICK_ATTRS:
        setattr(decorator, item, getattr(func, item, []))
    decorator.__doc__ = func.__doc__

    return decorator