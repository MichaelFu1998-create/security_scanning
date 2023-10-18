def build(ctx, docs=False):
    """Build the project."""
    cfg = config.load()
    ctx.run("python setup.py build")

    if docs:
        for doc_path in ('docs', 'doc'):
            if os.path.exists(cfg.rootjoin(doc_path, 'conf.py')):
                break
        else:
            doc_path = None

        if doc_path:
            ctx.run("invoke docs")
        else:
            notify.warning("Cannot find either a 'docs' or 'doc' Sphinx directory!")