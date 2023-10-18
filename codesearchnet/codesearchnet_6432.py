def mutate_file(backup, context):
    """
    :type backup: bool
    :type context: Context
    """
    with open(context.filename) as f:
        code = f.read()
    context.source = code
    if backup:
        with open(context.filename + '.bak', 'w') as f:
            f.write(code)
    result, number_of_mutations_performed = mutate(context)
    with open(context.filename, 'w') as f:
        f.write(result)
    return number_of_mutations_performed