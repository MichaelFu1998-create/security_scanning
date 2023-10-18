def reuse(context, block_list, **kwargs):
    '''
    Allow reuse of a block within a template.

    {% reuse '_myblock' foo=bar %}

    If passed a list of block names, will use the first that matches:

    {% reuse list_of_block_names .... %}
    '''
    try:
        block_context = context.render_context[BLOCK_CONTEXT_KEY]
    except KeyError:
        block_context = BlockContext()

    if not isinstance(block_list, (list, tuple)):
        block_list = [block_list]

    for block in block_list:
        block = block_context.get_block(block)
        if block:
            break
    else:
        return ''

    with context.push(kwargs):
        return block.render(context)