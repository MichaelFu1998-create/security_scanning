def infer(pattern, base_path=None):
    """https://github.com/frictionlessdata/datapackage-py#infer
    """
    package = Package({}, base_path=base_path)
    descriptor = package.infer(pattern)
    return descriptor