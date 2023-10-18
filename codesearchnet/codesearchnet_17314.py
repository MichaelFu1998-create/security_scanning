def serialize_namespaces(namespaces, connection: str, path, directory):
    """Parse a BEL document then serializes the given namespaces (errors and all) to the given directory."""
    from .definition_utils import export_namespaces

    graph = from_lines(path, manager=connection)
    export_namespaces(namespaces, graph, directory)