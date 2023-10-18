def clean(_dummy_ctx, docs=False, backups=False, bytecode=False, dist=False, # pylint: disable=redefined-outer-name
        all=False, venv=False, tox=False, extra=''): # pylint: disable=redefined-builtin
    """Perform house-keeping."""
    cfg = config.load()
    notify.banner("Cleaning up project files")

    # Add patterns based on given parameters
    venv_dirs = ['bin', 'include', 'lib', 'share', 'local', '.venv']
    patterns = ['build/', 'pip-selfcheck.json']
    excludes = ['.git/', '.hg/', '.svn/', 'debian/*/']
    if docs or all:
        patterns.extend(['docs/_build/', 'doc/_build/'])
    if dist or all:
        patterns.append('dist/')
    if backups or all:
        patterns.extend(['**/*~'])
    if bytecode or all:
        patterns.extend([
            '**/*.py[co]', '**/__pycache__/', '*.egg-info/',
            cfg.srcjoin('*.egg-info/')[len(cfg.project_root)+1:],
        ])
    if venv:
        patterns.extend([i + '/' for i in venv_dirs])
    if tox:
        patterns.append('.tox/')
    else:
        excludes.append('.tox/')
    if extra:
        patterns.extend(shlex.split(extra))

    # Build fileset
    patterns = [antglob.includes(i) for i in patterns] + [antglob.excludes(i) for i in excludes]
    if not venv:
        # Do not scan venv dirs when not cleaning them
        patterns.extend([antglob.excludes(i + '/') for i in venv_dirs])
    fileset = antglob.FileSet(cfg.project_root, patterns)

    # Iterate over matches and remove them
    for name in fileset:
        notify.info('rm {0}'.format(name))
        if name.endswith('/'):
            shutil.rmtree(os.path.join(cfg.project_root, name))
        else:
            os.unlink(os.path.join(cfg.project_root, name))