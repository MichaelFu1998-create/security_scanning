def pull_datapackage(descriptor, name, backend, **backend_options):
    """Pull Data Package from storage.

    All parameters should be used as keyword arguments.

    Args:
        descriptor (str): path where to store descriptor
        name (str): name of the pulled datapackage
        backend (str): backend name like `sql` or `bigquery`
        backend_options (dict): backend options mentioned in backend docs

    """

    # Deprecated
    warnings.warn(
        'Functions "push/pull_datapackage" are deprecated. '
        'Please use "Package" class',
        UserWarning)

    # Save datapackage name
    datapackage_name = name

    # Get storage
    plugin = import_module('jsontableschema.plugins.%s' % backend)
    storage = plugin.Storage(**backend_options)

    # Iterate over tables
    resources = []
    for table in storage.buckets:

        # Prepare
        schema = storage.describe(table)
        base = os.path.dirname(descriptor)
        path, name = _restore_path(table)
        fullpath = os.path.join(base, path)

        # Write data
        helpers.ensure_dir(fullpath)
        with io.open(fullpath, 'wb') as file:
            model = Schema(deepcopy(schema))
            data = storage.iter(table)
            writer = csv.writer(file, encoding='utf-8')
            writer.writerow(model.headers)
            for row in data:
                writer.writerow(row)

        # Add resource
        resource = {'schema': schema, 'path': path}
        if name is not None:
            resource['name'] = name
        resources.append(resource)

    # Write descriptor
    mode = 'w'
    encoding = 'utf-8'
    if six.PY2:
        mode = 'wb'
        encoding = None
    resources = _restore_resources(resources)
    helpers.ensure_dir(descriptor)
    with io.open(descriptor,
                 mode=mode,
                 encoding=encoding) as file:
        descriptor = {
            'name': datapackage_name,
            'resources': resources,
        }
        json.dump(descriptor, file, indent=4)
    return storage