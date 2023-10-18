def migrate(src_path,
            src_passphrase,
            src_backend,
            dst_path,
            dst_passphrase,
            dst_backend):
    """Migrate all keys in a source stash to a destination stash

    The migration process will decrypt all keys using the source
    stash's passphrase and then encrypt them based on the destination
    stash's passphrase.

    re-encryption will take place only if the passphrases are differing
    """
    src_storage = STORAGE_MAPPING[src_backend](**_parse_path_string(src_path))
    dst_storage = STORAGE_MAPPING[dst_backend](**_parse_path_string(dst_path))
    src_stash = Stash(src_storage, src_passphrase)
    dst_stash = Stash(dst_storage, dst_passphrase)
    # TODO: Test that re-encryption does not occur on similar
    # passphrases
    keys = src_stash.export()
    dst_stash.load(src_passphrase, keys=keys)