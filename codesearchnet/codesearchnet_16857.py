def setup(app):
    """Hook the directives when Sphinx ask for it."""
    if 'http' not in app.domains:
        httpdomain.setup(app)

    app.add_directive('autopyramid', RouteDirective)