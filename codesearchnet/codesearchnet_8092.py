def upload(args):
    """Upload a new file to an existing project.

    The first part of the remote path is interpreted as the name of the
    storage provider. If there is no match the default (osfstorage) is
    used.

    If the project is private you need to specify a username.

    To upload a whole directory (and all its sub-directories) use the `-r`
    command-line option. If your source directory name ends in a / then
    files will be created directly in the remote directory. If it does not
    end in a slash an extra sub-directory with the name of the local directory
    will be created.

    To place contents of local directory `foo` in remote directory `bar/foo`:
    $ osf upload -r foo bar
    To place contents of local directory `foo` in remote directory `bar`:
    $ osf upload -r foo/ bar
    """
    osf = _setup_osf(args)
    if osf.username is None or osf.password is None:
        sys.exit('To upload a file you need to provide a username and'
                 ' password.')

    project = osf.project(args.project)
    storage, remote_path = split_storage(args.destination)

    store = project.storage(storage)
    if args.recursive:
        if not os.path.isdir(args.source):
            raise RuntimeError("Expected source ({}) to be a directory when "
                               "using recursive mode.".format(args.source))

        # local name of the directory that is being uploaded
        _, dir_name = os.path.split(args.source)

        for root, _, files in os.walk(args.source):
            subdir_path = os.path.relpath(root, args.source)
            for fname in files:
                local_path = os.path.join(root, fname)
                with open(local_path, 'rb') as fp:
                    # build the remote path + fname
                    name = os.path.join(remote_path, dir_name, subdir_path,
                                        fname)
                    store.create_file(name, fp, force=args.force,
                                      update=args.update)

    else:
        with open(args.source, 'rb') as fp:
            store.create_file(remote_path, fp, force=args.force,
                              update=args.update)