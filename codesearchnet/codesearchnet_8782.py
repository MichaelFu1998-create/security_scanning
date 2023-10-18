def setup(app):
    """Sphinx extension: run sphinx-apidoc."""
    event = 'builder-inited' if six.PY3 else b'builder-inited'
    app.connect(event, on_init)