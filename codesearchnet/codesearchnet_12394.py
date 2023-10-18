def setup_paths(source, destination, name, add_to_global, force):
    """
    Determine source and destination using the options.
    """
    if source[-1] == "/":
        source = source[:-1]
    if not name:
        name = os.path.split(source)[-1]
    elif name.endswith(".docset"):
        name = name.replace(".docset", "")
    if add_to_global:
        destination = DEFAULT_DOCSET_PATH
    dest = os.path.join(destination or "", name + ".docset")
    dst_exists = os.path.lexists(dest)
    if dst_exists and force:
        shutil.rmtree(dest)
    elif dst_exists:
        log.error(
            'Destination path "{}" already exists.'.format(
                click.format_filename(dest)
            )
        )
        raise SystemExit(errno.EEXIST)
    return source, dest, name