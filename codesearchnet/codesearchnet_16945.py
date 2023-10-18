def ci(ctx):
    """Perform continuous integration tasks."""
    opts = ['']

    # 'tox' makes no sense in Travis
    if os.environ.get('TRAVIS', '').lower() == 'true':
        opts += ['test.pytest']
    else:
        opts += ['test.tox']

    ctx.run("invoke --echo --pty clean --all build --docs check --reports{}".format(' '.join(opts)))