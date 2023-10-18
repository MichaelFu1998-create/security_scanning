def group(ctx, project, group):  # pylint:disable=redefined-outer-name
    """Commands for experiment groups."""
    ctx.obj = ctx.obj or {}
    ctx.obj['project'] = project
    ctx.obj['group'] = group