def bookmark(ctx, username):  # pylint:disable=redefined-outer-name
    """Commands for bookmarks."""
    ctx.obj = ctx.obj or {}
    ctx.obj['username'] = username