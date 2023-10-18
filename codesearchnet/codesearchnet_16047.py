def convert_completezip(path):
    """Converts a completezip file structure to a litezip file structure.
    Returns a litezip data structure.

    """
    for filepath in path.glob('**/index_auto_generated.cnxml'):
        filepath.rename(filepath.parent / 'index.cnxml')
        logger.debug('removed {}'.format(filepath))
    for filepath in path.glob('**/index.cnxml.html'):
        filepath.unlink()
    return parse_litezip(path)