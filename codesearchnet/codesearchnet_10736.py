def _build_backend():
    """Find and load the build backend"""
    # Add in-tree backend directories to the front of sys.path.
    backend_path = os.environ.get('PEP517_BACKEND_PATH')
    if backend_path:
        extra_pathitems = backend_path.split(os.pathsep)
        sys.path[:0] = extra_pathitems

    ep = os.environ['PEP517_BUILD_BACKEND']
    mod_path, _, obj_path = ep.partition(':')
    try:
        obj = import_module(mod_path)
    except ImportError:
        raise BackendUnavailable(traceback.format_exc())

    if backend_path:
        if not any(
            contained_in(obj.__file__, path)
            for path in extra_pathitems
        ):
            raise BackendInvalid("Backend was not loaded from backend-path")

    if obj_path:
        for path_part in obj_path.split('.'):
            obj = getattr(obj, path_part)
    return obj