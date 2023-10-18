def render_to(path, template, **data):
    """shortcut to render data with `template` and then write to `path`.
    Just add exception catch to `renderer.render_to`"""
    try:
        renderer.render_to(path, template, **data)
    except JinjaTemplateNotFound as e:
        logger.error(e.__doc__ + ', Template: %r' % template)
        sys.exit(e.exit_code)