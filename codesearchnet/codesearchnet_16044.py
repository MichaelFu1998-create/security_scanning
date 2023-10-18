def parse_module(path, excludes=None):
    """Parse the file structure to a data structure given the path to
    a module directory.

    """
    file = path / MODULE_FILENAME

    if not file.exists():
        raise MissingFile(file)
    id = _parse_document_id(etree.parse(file.open()))

    excludes = excludes or []
    excludes.extend([
        lambda filepath: filepath.name == MODULE_FILENAME,
    ])

    resources_paths = _find_resources(path, excludes=excludes)
    resources = tuple(_resource_from_path(res) for res in resources_paths)

    return Module(id, file, resources)