def build(ctx, dput='', opts=''):
    """Build a DEB package."""
    # Get package metadata
    with io.open('debian/changelog', encoding='utf-8') as changes:
        metadata = re.match(r'^([^ ]+) \(([^)]+)\) ([^;]+); urgency=(.+)$', changes.readline().rstrip())
        if not metadata:
            notify.failure('Badly formatted top entry in changelog')
        name, version, _, _ = metadata.groups()

    # Build package
    ctx.run('dpkg-buildpackage {} {}'.format(ctx.rituals.deb.build.opts, opts))

    # Move created artifacts into "dist"
    if not os.path.exists('dist'):
        os.makedirs('dist')
    artifact_pattern = '{}?{}*'.format(name, re.sub(r'[^-_.a-zA-Z0-9]', '?', version))
    changes_files = []
    for debfile in glob.glob('../' + artifact_pattern):
        shutil.move(debfile, 'dist')
        if debfile.endswith('.changes'):
            changes_files.append(os.path.join('dist', os.path.basename(debfile)))
    ctx.run('ls -l dist/{}'.format(artifact_pattern))

    if dput:
        ctx.run('dput {} {}'.format(dput, ' '.join(changes_files)))