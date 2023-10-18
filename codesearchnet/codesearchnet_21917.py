def ensure_path_exists(path, *args):
    '''Like os.makedirs but keeps quiet if path already exists'''
    if os.path.exists(path):
        return

    os.makedirs(path, *args)