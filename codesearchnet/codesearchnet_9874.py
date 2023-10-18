def push_datapackage(descriptor, backend, **backend_options):
    """Push Data Package to storage.

    All parameters should be used as keyword arguments.

    Args:
        descriptor (str): path to descriptor
        backend (str): backend name like `sql` or `bigquery`
        backend_options (dict): backend options mentioned in backend docs

    """

    # Deprecated
    warnings.warn(
        'Functions "push/pull_datapackage" are deprecated. '
        'Please use "Package" class',
        UserWarning)

    # Init maps
    tables = []
    schemas = []
    datamap = {}
    mapping = {}

    # Init model
    model = Package(descriptor)

    # Get storage
    plugin = import_module('jsontableschema.plugins.%s' % backend)
    storage = plugin.Storage(**backend_options)

    # Collect tables/schemas/data
    for resource in model.resources:
        if not resource.tabular:
            continue
        name = resource.descriptor.get('name', None)
        table = _convert_path(resource.descriptor['path'], name)
        schema = resource.descriptor['schema']
        data = resource.table.iter(keyed=True)
        # TODO: review
        def values(schema, data):
            for item in data:
                row = []
                for field in schema['fields']:
                    row.append(item.get(field['name'], None))
                yield tuple(row)
        tables.append(table)
        schemas.append(schema)
        datamap[table] = values(schema, data)
        if name is not None:
            mapping[name] = table
    schemas = _convert_schemas(mapping, schemas)

    # Create tables
    for table in tables:
        if table in storage.buckets:
            storage.delete(table)
    storage.create(tables, schemas)

    # Write data to tables
    for table in storage.buckets:
        if table in datamap:
            storage.write(table, datamap[table])
    return storage