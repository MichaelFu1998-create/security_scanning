def find_block(context, *names):
    '''
    Find the first matching block in the current block_context
    '''
    block_set = context.render_context[BLOCK_CONTEXT_KEY]
    for name in names:
        block = block_set.get_block(name)
        if block is not None:
            return block

    raise template.TemplateSyntaxError('No widget found for: %r' % (names,))