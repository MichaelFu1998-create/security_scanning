def experiment(ctx, project, experiment):  # pylint:disable=redefined-outer-name
    """Commands for experiments."""
    ctx.obj = ctx.obj or {}
    ctx.obj['project'] = project
    ctx.obj['experiment'] = experiment