def fetch(args):
    """Fetch an individual file from a project.

    The first part of the remote path is interpreted as the name of the
    storage provider. If there is no match the default (osfstorage) is
    used.

    The local path defaults to the name of the remote file.

    If the project is private you need to specify a username.

    If args.force is True, write local file even if that file already exists.
    If args.force is False but args.update is True, overwrite an existing local
    file only if local and remote files differ.
    """
    storage, remote_path = split_storage(args.remote)

    local_path = args.local
    if local_path is None:
        _, local_path = os.path.split(remote_path)

    local_path_exists = os.path.exists(local_path)
    if local_path_exists and not args.force and not args.update:
        sys.exit("Local file %s already exists, not overwriting." % local_path)

    directory, _ = os.path.split(local_path)
    if directory:
        makedirs(directory, exist_ok=True)

    osf = _setup_osf(args)
    project = osf.project(args.project)

    store = project.storage(storage)
    for file_ in store.files:
        if norm_remote_path(file_.path) == remote_path:
            if local_path_exists and not args.force and args.update:
                if file_.hashes.get('md5') == checksum(local_path):
                    print("Local file %s already matches remote." % local_path)
                    break
            with open(local_path, 'wb') as fp:
                file_.write_to(fp)

            # only fetching one file so we are done
            break