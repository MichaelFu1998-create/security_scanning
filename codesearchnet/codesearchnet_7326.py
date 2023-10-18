def _move_temp_binary_to_path(tmp_binary_path):
    """Moves the temporary binary to the location of the binary that's currently being run.
    Preserves owner, group, and permissions of original binary"""
    # pylint: disable=E1101
    binary_path = _get_binary_location()
    if not binary_path.endswith(constants.DUSTY_BINARY_NAME):
        raise RuntimeError('Refusing to overwrite binary {}'.format(binary_path))
    st = os.stat(binary_path)
    permissions = st.st_mode
    owner = st.st_uid
    group = st.st_gid
    shutil.move(tmp_binary_path, binary_path)
    os.chown(binary_path, owner, group)
    os.chmod(binary_path, permissions)
    return binary_path