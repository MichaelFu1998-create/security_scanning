def create_application(connection: Optional[str] = None) -> Flask:
    """Create a Flask application."""
    app = Flask(__name__)

    flask_bootstrap.Bootstrap(app)
    Admin(app)

    connection = connection or DEFAULT_CACHE_CONNECTION
    engine, session = build_engine_session(connection)

    for name, add_admin in add_admins.items():
        url = '/{}'.format(name)
        add_admin(app, session, url=url, endpoint=name, name=name)
        log.debug('added %s - %s to %s', name, add_admin, url)

    app.register_blueprint(ui)

    return app