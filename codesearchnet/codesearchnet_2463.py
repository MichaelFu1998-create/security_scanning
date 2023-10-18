def clone(git_uri):
    """
    Clone a remote git repository to a local path.

    :param git_uri: the URI to the git repository to be cloned
    :return: the generated local path where the repository has been cloned to
    """
    hash_digest = sha256_hash(git_uri)
    local_path = home_directory_path(FOLDER, hash_digest)
    exists_locally = path_exists(local_path)

    if not exists_locally:
        _clone_repo(git_uri, local_path)
    else:
        logging.info(  # pragma: no cover
            "Git repository already exists locally.")  # pragma: no cover

    return local_path