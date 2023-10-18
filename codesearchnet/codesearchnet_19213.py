def init_app(self, app, **kwargs):
        """Initialize application object.

        :param app: An instance of :class:`~flask.Flask`.
        """
        # Init the configuration
        self.init_config(app)
        # Enable Rate limiter
        self.limiter = Limiter(app, key_func=get_ipaddr)
        # Enable secure HTTP headers
        if app.config['APP_ENABLE_SECURE_HEADERS']:
            self.talisman = Talisman(
                app, **app.config.get('APP_DEFAULT_SECURE_HEADERS', {})
            )
        # Enable PING view
        if app.config['APP_HEALTH_BLUEPRINT_ENABLED']:
            blueprint = Blueprint('invenio_app_ping', __name__)

            @blueprint.route('/ping')
            def ping():
                """Load balancer ping view."""
                return 'OK'

            ping.talisman_view_options = {'force_https': False}

            app.register_blueprint(blueprint)

        requestid_header = app.config.get('APP_REQUESTID_HEADER')
        if requestid_header:
            @app.before_request
            def set_request_id():
                """Extracts a request id from an HTTP header."""
                request_id = request.headers.get(requestid_header)
                if request_id:
                    # Capped at 200 to protect against malicious clients
                    # sending very large headers.
                    g.request_id = request_id[:200]

        # If installed register the Flask-DebugToolbar extension
        try:
            from flask_debugtoolbar import DebugToolbarExtension
            app.extensions['flask-debugtoolbar'] = DebugToolbarExtension(app)
        except ImportError:
            app.logger.debug('Flask-DebugToolbar extension not installed.')

        # Register self
        app.extensions['invenio-app'] = self