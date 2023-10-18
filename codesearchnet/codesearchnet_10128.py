def _ca_path(temp_dir=None):
    """
    Returns the file path to the CA certs file

    :param temp_dir:
        The temporary directory to cache the CA certs in on OS X and Windows.
        Needs to have secure permissions so other users can not modify the
        contents.

    :return:
        A 2-element tuple:
         - 0: A unicode string of the file path
         - 1: A bool if the file is a temporary file
    """

    ca_path = system_path()

    # Windows and OS X
    if ca_path is None:
        if temp_dir is None:
            temp_dir = tempfile.gettempdir()

        if not os.path.isdir(temp_dir):
            raise CACertsError(pretty_message(
                '''
                The temp dir specified, "%s", is not a directory
                ''',
                temp_dir
            ))

        ca_path = os.path.join(temp_dir, 'oscrypto-ca-bundle.crt')
        return (ca_path, True)

    return (ca_path, False)