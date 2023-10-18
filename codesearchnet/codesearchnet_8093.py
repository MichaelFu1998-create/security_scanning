def remove(args):
    """Remove a file from the project's storage.

    The first part of the remote path is interpreted as the name of the
    storage provider. If there is no match the default (osfstorage) is
    used.
    """
    osf = _setup_osf(args)
    if osf.username is None or osf.password is None:
        sys.exit('To remove a file you need to provide a username and'
                 ' password.')

    project = osf.project(args.project)

    storage, remote_path = split_storage(args.target)

    store = project.storage(storage)
    for f in store.files:
        if norm_remote_path(f.path) == remote_path:
            f.remove()