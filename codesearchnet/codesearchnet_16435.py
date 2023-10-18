def job(ctx, project, job):  # pylint:disable=redefined-outer-name
    """Commands for jobs."""
    ctx.obj = ctx.obj or {}
    ctx.obj['project'] = project
    ctx.obj['job'] = job