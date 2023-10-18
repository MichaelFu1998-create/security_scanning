def dump_config():
    """Print out all the config information we have so far (for debugging)."""
    print('PyAV:', version, git_commit or '(unknown commit)')
    print('Python:', sys.version.encode('unicode_escape' if PY3 else 'string-escape'))
    print('platform:', platform.platform())
    print('extension_extra:')
    for k, vs in extension_extra.items():
        print('\t%s: %s' % (k, [x.encode('utf8') for x in vs]))
    print('config_macros:')
    for x in sorted(config_macros.items()):
        print('\t%s=%s' % x)