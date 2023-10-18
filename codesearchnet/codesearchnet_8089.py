def clone(args):
    """Copy all files from all storages of a project.

    The output directory defaults to the current directory.

    If the project is private you need to specify a username.

    If args.update is True, overwrite any existing local files only if local and
    remote files differ.
    """
    osf = _setup_osf(args)
    project = osf.project(args.project)
    output_dir = args.project
    if args.output is not None:
        output_dir = args.output

    with tqdm(unit='files') as pbar:
        for store in project.storages:
            prefix = os.path.join(output_dir, store.name)

            for file_ in store.files:
                path = file_.path
                if path.startswith('/'):
                    path = path[1:]

                path = os.path.join(prefix, path)
                if os.path.exists(path) and args.update:
                    if checksum(path) == file_.hashes.get('md5'):
                        continue
                directory, _ = os.path.split(path)
                makedirs(directory, exist_ok=True)

                with open(path, "wb") as f:
                    file_.write_to(f)

                pbar.update()