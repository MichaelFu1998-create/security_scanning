def iter_cython(path):
    '''Yield all ``.pyx`` and ``.pxd`` files in the given root.'''
    for dir_path, dir_names, file_names in os.walk(path):
        for file_name in file_names:
            if file_name.startswith('.'):
                continue
            if os.path.splitext(file_name)[1] not in ('.pyx', '.pxd'):
                continue
            yield os.path.join(dir_path, file_name)