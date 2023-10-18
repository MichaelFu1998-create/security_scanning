def load_widgets(context, **kwargs):
    '''
    Load a series of widget libraries.
    '''
    _soft = kwargs.pop('_soft', False)

    try:
        widgets = context.render_context[WIDGET_CONTEXT_KEY]
    except KeyError:
        widgets = context.render_context[WIDGET_CONTEXT_KEY] = {}

    for alias, template_name in kwargs.items():
        if _soft and alias in widgets:
            continue

        with context.render_context.push({BLOCK_CONTEXT_KEY: BlockContext()}):
            blocks = resolve_blocks(template_name, context)
            widgets[alias] = blocks

    return ''