def render(template, **data):
    """shortcut to render data with `template`. Just add exception
    catch to `renderer.render`"""
    try:
        return renderer.render(template, **data)
    except JinjaTemplateNotFound as e:
        logger.error(e.__doc__ + ', Template: %r' % template)
        sys.exit(e.exit_code)