def add_mutations_by_file(mutations_by_file, filename, exclude, dict_synonyms):
    """
    :type mutations_by_file: dict[str, list[MutationID]]
    :type filename: str
    :type exclude: Callable[[Context], bool]
    :type dict_synonyms: list[str]
    """
    with open(filename) as f:
        source = f.read()
    context = Context(
        source=source,
        filename=filename,
        exclude=exclude,
        dict_synonyms=dict_synonyms,
    )

    try:
        mutations_by_file[filename] = list_mutations(context)
        register_mutants(mutations_by_file)
    except Exception as e:
        raise RuntimeError('Failed while creating mutations for %s, for line "%s"' % (context.filename, context.current_source_line), e)