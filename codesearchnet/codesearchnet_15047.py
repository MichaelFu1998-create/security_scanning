def load():
    """ Load and return configuration as a ``Bunch``.

        Values are based on ``DEFAULTS``, and metadata from ``setup.py``.
    """
    cfg = Bunch(DEFAULTS)
    # TODO: override with contents of [rituals] section in setup.cfg

    cfg.project_root = get_project_root()
    if not cfg.project_root:
        raise RuntimeError("No tasks module is imported, cannot determine project root")

    cfg.rootjoin = lambda *names: os.path.join(cfg.project_root, *names)
    cfg.srcjoin = lambda *names: cfg.rootjoin(cfg.srcdir, *names)
    cfg.testjoin = lambda *names: cfg.rootjoin(cfg.testdir, *names)
    cfg.cwd = os.getcwd()
    os.chdir(cfg.project_root)

    # this assumes an importable setup.py
    # TODO: maybe call "python setup.py egg_info" for metadata
    if cfg.project_root not in sys.path:
        sys.path.append(cfg.project_root)
    try:
        from setup import project # pylint: disable=no-name-in-module
    except ImportError:
        from setup import setup_args as project # pylint: disable=no-name-in-module
    cfg.project = Bunch(project)

    return cfg