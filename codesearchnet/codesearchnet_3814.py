def unified_job_template_options(method):
    """
    Adds the decorators for all types of unified job templates,
    and if the non-unified type is specified, converts it into the
    unified_job_template kwarg.
    """
    jt_dec = click.option(
        '--job-template', type=types.Related('job_template'),
        help='Use this job template as unified_job_template field')
    prj_dec = click.option(
        '--project', type=types.Related('project'),
        help='Use this project as unified_job_template field')
    inv_src_dec = click.option(
        '--inventory-source', type=types.Related('inventory_source'),
        help='Use this inventory source as unified_job_template field')

    def ujt_translation(_method):
        def _ujt_translation(*args, **kwargs):
            for fd in ['job_template', 'project', 'inventory_source']:
                if fd in kwargs and kwargs[fd] is not None:
                    kwargs['unified_job_template'] = kwargs.pop(fd)
            return _method(*args, **kwargs)
        return functools.wraps(_method)(_ujt_translation)

    return ujt_translation(
        inv_src_dec(
            prj_dec(
                jt_dec(
                    method
                )
            )
        )
    )