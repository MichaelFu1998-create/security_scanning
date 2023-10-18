def get_version():
    """
    Get the version from version module without importing more than
    necessary.
    """
    version_module_path = os.path.join(
        os.path.dirname(__file__), "txspinneret", "_version.py")
    # The version module contains a variable called __version__
    with open(version_module_path) as version_module:
        exec(version_module.read())
    return locals()["__version__"]