def get_all_keyring():
    """
    Return a list of all implemented keyrings that can be constructed without
    parameters.
    """
    _load_plugins()
    viable_classes = KeyringBackend.get_viable_backends()
    rings = util.suppress_exceptions(viable_classes, exceptions=TypeError)
    return list(rings)