def embed_code_links(app, exception):
    """Embed hyperlinks to documentation into example code"""
    if exception is not None:
        return

    # No need to waste time embedding hyperlinks when not running the examples
    # XXX: also at the time of writing this fixes make html-noplot
    # for some reason I don't fully understand
    if not app.builder.config.plot_gallery:
        return

    # XXX: Whitelist of builders for which it makes sense to embed
    # hyperlinks inside the example html. Note that the link embedding
    # require searchindex.js to exist for the links to the local doc
    # and there does not seem to be a good way of knowing which
    # builders creates a searchindex.js.
    if app.builder.name not in ['html', 'readthedocs']:
        return

    print('Embedding documentation hyperlinks in examples..')

    gallery_conf = app.config.sphinx_gallery_conf

    gallery_dirs = gallery_conf['gallery_dirs']
    if not isinstance(gallery_dirs, list):
        gallery_dirs = [gallery_dirs]

    for gallery_dir in gallery_dirs:
        _embed_code_links(app, gallery_conf, gallery_dir)