def render_toolbar(context, config):
    """Render the toolbar for the given config."""
    quill_config = getattr(quill_app, config)
    t = template.loader.get_template(quill_config['toolbar_template'])
    return t.render(context)