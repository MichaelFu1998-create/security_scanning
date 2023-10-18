def parse_collection(path, excludes=None):
    """Parse a file structure to a data structure given the path to
    a collection directory.

    """
    file = path / COLLECTION_FILENAME
    if not file.exists():
        raise MissingFile(file)
    id = _parse_document_id(etree.parse(file.open()))

    excludes = excludes or []
    excludes.extend([
        lambda filepath: filepath.name == COLLECTION_FILENAME,
        lambda filepath: filepath.is_dir(),
    ])
    resources_paths = _find_resources(path, excludes=excludes)
    resources = tuple(_resource_from_path(res) for res in resources_paths)

    return Collection(id, file, resources)