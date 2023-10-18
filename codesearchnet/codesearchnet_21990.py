def schema(args):
    """Run South's schemamigration command.
    """
    try:
        import south
        cmd = args and 'schemamigration %s' % ' '.join(options.args) or 'schemamigration'
        call_manage(cmd)
    except ImportError:
        error('Could not import south.')