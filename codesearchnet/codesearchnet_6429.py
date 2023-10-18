def mutate(context):
    """
    :type context: Context
    :return: tuple: mutated source code, number of mutations performed
    :rtype: tuple[str, int]
    """
    try:
        result = parse(context.source, error_recovery=False)
    except Exception:
        print('Failed to parse %s. Internal error from parso follows.' % context.filename)
        print('----------------------------------')
        raise
    mutate_list_of_nodes(result, context=context)
    mutated_source = result.get_code().replace(' not not ', ' ')
    if context.remove_newline_at_end:
        assert mutated_source[-1] == '\n'
        mutated_source = mutated_source[:-1]
    if context.number_of_performed_mutations:
        # If we said we mutated the code, check that it has actually changed
        assert context.source != mutated_source
    context.mutated_source = mutated_source
    return mutated_source, context.number_of_performed_mutations