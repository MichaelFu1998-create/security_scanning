def sheet(connection, skip, file: TextIO):
    """Generate a summary sheet."""
    from tabulate import tabulate
    header = ['', 'Name', 'Description', 'Terms', 'Relations']
    rows = []

    for i, (idx, name, manager) in enumerate(_iterate_managers(connection, skip), start=1):
        try:
            if not manager.is_populated():
                continue
        except AttributeError:
            click.secho(f'{name} does not implement is_populated', fg='red')
            continue

        terms, relations = None, None
        if isinstance(manager, BELNamespaceManagerMixin):
            terms = manager._count_model(manager.namespace_model)

        if isinstance(manager, BELManagerMixin):
            try:
                relations = manager.count_relations()
            except TypeError as e:
                relations = str(e)

        rows.append((i, name, manager.__doc__.split('\n')[0].strip().strip('.'), terms, relations))

    print(tabulate(
        rows,
        headers=header,
        # tablefmt="fancy_grid",
    ))