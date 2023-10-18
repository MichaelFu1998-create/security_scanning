def generate_gallery_rst(app):
    """Generate the Main examples gallery reStructuredText

    Start the sphinx-gallery configuration and recursively scan the examples
    directories in order to populate the examples gallery
    """
    try:
        plot_gallery = eval(app.builder.config.plot_gallery)
    except TypeError:
        plot_gallery = bool(app.builder.config.plot_gallery)

    gallery_conf.update(app.config.sphinx_gallery_conf)
    gallery_conf.update(plot_gallery=plot_gallery)
    gallery_conf.update(abort_on_example_error=app.builder.config.abort_on_example_error)

    # this assures I can call the config in other places
    app.config.sphinx_gallery_conf = gallery_conf
    app.config.html_static_path.append(glr_path_static())

    clean_gallery_out(app.builder.outdir)

    examples_dirs = gallery_conf['examples_dirs']
    gallery_dirs = gallery_conf['gallery_dirs']

    if not isinstance(examples_dirs, list):
        examples_dirs = [examples_dirs]
    if not isinstance(gallery_dirs, list):
        gallery_dirs = [gallery_dirs]

    mod_examples_dir = os.path.relpath(gallery_conf['mod_example_dir'],
                                       app.builder.srcdir)
    seen_backrefs = set()

    for examples_dir, gallery_dir in zip(examples_dirs, gallery_dirs):
        examples_dir = os.path.relpath(examples_dir,
                                       app.builder.srcdir)
        gallery_dir = os.path.relpath(gallery_dir,
                                      app.builder.srcdir)

        for workdir in [examples_dir, gallery_dir, mod_examples_dir]:
            if not os.path.exists(workdir):
                os.makedirs(workdir)

        # we create an index.rst with all examples
        fhindex = open(os.path.join(gallery_dir, 'index.rst'), 'w')
        # Here we don't use an os.walk, but we recurse only twice: flat is
        # better than nested.
        fhindex.write(generate_dir_rst(examples_dir, gallery_dir, gallery_conf,
                                       seen_backrefs))
        for directory in sorted(os.listdir(examples_dir)):
            if os.path.isdir(os.path.join(examples_dir, directory)):
                src_dir = os.path.join(examples_dir, directory)
                target_dir = os.path.join(gallery_dir, directory)
                fhindex.write(generate_dir_rst(src_dir, target_dir,
                                               gallery_conf,
                                               seen_backrefs))
        fhindex.flush()