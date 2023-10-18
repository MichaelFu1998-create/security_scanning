def walk_up(start_dir, depth=20):
    '''
    Walk up a directory tree
    '''
    root = start_dir

    for i in xrange(depth):
        contents = os.listdir(root)
        subdirs, files = [], []
        for f in contents:
            if os.path.isdir(os.path.join(root, f)):
                subdirs.append(f)
            else:
                files.append(f)

        yield root, subdirs, files

        parent = os.path.dirname(root)
        if parent and not parent == root:
            root = parent
        else:
            break