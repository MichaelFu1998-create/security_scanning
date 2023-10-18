def walk_dn(start_dir, depth=10):
    '''
    Walk down a directory tree. Same as os.walk but allows for a depth limit
    via depth argument
    '''

    start_depth = len(os.path.split(start_dir))
    end_depth = start_depth + depth

    for root, subdirs, files in os.walk(start_dir):
        yield root, subdirs, files

        if len(os.path.split(root)) >= end_depth:
            break