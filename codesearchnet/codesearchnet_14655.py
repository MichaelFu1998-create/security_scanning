def migrate_stash(source_stash_path,
                  source_passphrase,
                  source_backend,
                  destination_stash_path,
                  destination_passphrase,
                  destination_backend):
    """Migrate all keys from a source stash to a destination stash.

    `SOURCE_STASH_PATH` and `DESTINATION_STASH_PATH` are the paths
    to the stashs you wish to perform the migration on.
    """
    click.echo('Migrating all keys from {0} to {1}...'.format(
        source_stash_path, destination_stash_path))

    try:
        migrate(
            src_path=source_stash_path,
            src_passphrase=source_passphrase,
            src_backend=source_backend,
            dst_path=destination_stash_path,
            dst_passphrase=destination_passphrase,
            dst_backend=destination_backend)
    except GhostError as ex:
        sys.exit(ex)
    click.echo('Migration complete!')