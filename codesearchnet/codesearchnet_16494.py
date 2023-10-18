def project(ctx, project):  # pylint:disable=redefined-outer-name
    """Commands for projects."""
    if ctx.invoked_subcommand not in ['create', 'list']:
        ctx.obj = ctx.obj or {}
        ctx.obj['project'] = project