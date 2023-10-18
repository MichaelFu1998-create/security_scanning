def confluence(ctx, no_publish=False, clean=False, opts=''):
    """Build Sphinx docs and publish to Confluence."""
    cfg = config.load()

    if clean:
        ctx.run("invoke clean --docs")

    cmd = ['sphinx-build', '-b', 'confluence']
    cmd.extend(['-E', '-a'])  # force a full rebuild
    if opts:
        cmd.append(opts)
    cmd.extend(['.', ctx.rituals.docs.build + '_cf'])
    if no_publish:
        cmd.extend(['-Dconfluence_publish=False'])

    # Build docs
    notify.info("Starting Sphinx build...")
    with pushd(ctx.rituals.docs.sources):
        ctx.run(' '.join(cmd), pty=True)