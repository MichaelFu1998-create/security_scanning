def setup(app):
    """Setup sphinx-gallery sphinx extension"""
    app.add_config_value('plot_gallery', True, 'html')
    app.add_config_value('abort_on_example_error', False, 'html')
    app.add_config_value('sphinx_gallery_conf', gallery_conf, 'html')
    app.add_stylesheet('gallery.css')

    app.connect('builder-inited', generate_gallery_rst)

    app.connect('build-finished', embed_code_links)