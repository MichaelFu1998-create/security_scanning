def _cleanup_path(path):
    """Recursively delete a path upon exiting this context
    manager. Supports targets that are files or directories."""
    try:
        yield
    finally:
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)