def using(context, alias):
    '''
    Temporarily update the context to use the BlockContext for the given alias.
    '''

    # An empty alias means look in the current widget set.
    if alias == '':
        yield context
    else:
        try:
            widgets = context.render_context[WIDGET_CONTEXT_KEY]
        except KeyError:
            raise template.TemplateSyntaxError('No widget libraries loaded!')

        try:
            block_set = widgets[alias]
        except KeyError:
            raise template.TemplateSyntaxError('No widget library loaded for alias: %r' % alias)

        context.render_context.push()
        context.render_context[BLOCK_CONTEXT_KEY] = block_set
        context.render_context[WIDGET_CONTEXT_KEY] = widgets

        yield context

        context.render_context.pop()