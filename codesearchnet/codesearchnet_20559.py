def upload(ctx, repo):
    """Upload the package to an index server.

    This implies cleaning and re-building the package.

    :param repo: Required. Name of the index server to upload to, as specifies
        in your .pypirc configuration file.
    """
    artifacts = ' '.join(
        shlex.quote(str(n))
        for n in ROOT.joinpath('dist').glob('pipfile[-_]cli-*')
    )
    ctx.run(f'twine upload --repository="{repo}" {artifacts}')