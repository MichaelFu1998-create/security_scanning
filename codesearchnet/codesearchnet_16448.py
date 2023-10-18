def build(ctx, project, build):  # pylint:disable=redefined-outer-name
    """Commands for build jobs."""
    ctx.obj = ctx.obj or {}
    ctx.obj['project'] = project
    ctx.obj['build'] = build