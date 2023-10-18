def get_devpi_url(ctx):
    """Get currently used 'devpi' base URL."""
    cmd = 'devpi use --urls'
    lines = ctx.run(cmd, hide='out', echo=False).stdout.splitlines()
    for line in lines:
        try:
            line, base_url = line.split(':', 1)
        except ValueError:
            notify.warning('Ignoring "{}"!'.format(line))
        else:
            if line.split()[-1].strip() == 'simpleindex':
                return base_url.split('\x1b')[0].strip().rstrip('/')

    raise LookupError("Cannot find simpleindex URL in '{}' output:\n    {}".format(
        cmd, '\n    '.join(lines),
    ))