def init_storage_dir(storage_dir):
    """
    Initialise the storage directory with the certificates directory and a
    default wildcard self-signed certificate for HAProxy.

    :return: the storage path and certs path
    """
    storage_path = FilePath(storage_dir)

    # Create the default wildcard certificate if it doesn't already exist
    default_cert_path = storage_path.child('default.pem')
    if not default_cert_path.exists():
        default_cert_path.setContent(generate_wildcard_pem_bytes())

    # Create a directory for unmanaged certs. We don't touch this again, but it
    # needs to be there and it makes sense to create it at the same time as
    # everything else.
    unmanaged_certs_path = storage_path.child('unmanaged-certs')
    if not unmanaged_certs_path.exists():
        unmanaged_certs_path.createDirectory()

    # Store certificates in a directory inside the storage directory, so
    # HAProxy will read just the certificates there.
    certs_path = storage_path.child('certs')
    if not certs_path.exists():
        certs_path.createDirectory()

    return storage_path, certs_path