def export_keys(output_path, stash, passphrase, backend):
    """Export all keys to a file
    """
    stash = _get_stash(backend, stash, passphrase)

    try:
        click.echo('Exporting stash to {0}...'.format(output_path))
        stash.export(output_path=output_path)
        click.echo('Export complete!')
    except GhostError as ex:
        sys.exit(ex)