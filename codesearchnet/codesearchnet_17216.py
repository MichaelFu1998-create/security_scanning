def lint_directory(source, target):
    """Adds a linted version of each document in the source directory to the target directory

    :param str source: Path to directory to lint
    :param str target: Path to directory to output
    """
    for path in os.listdir(source):
        if not path.endswith('.bel'):
            continue

        log.info('linting: %s', path)
        with open(os.path.join(source, path)) as i, open(os.path.join(target, path), 'w') as o:
            lint_file(i, o)