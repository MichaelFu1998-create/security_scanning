def copy(src, dst, symlink=False, rellink=False):
    """Copy or symlink the file."""
    func = os.symlink if symlink else shutil.copy2
    if symlink and os.path.lexists(dst):
        os.remove(dst)
    if rellink:  # relative symlink from dst
        func(os.path.relpath(src, os.path.dirname(dst)), dst)
    else:
        func(src, dst)