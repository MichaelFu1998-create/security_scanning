def init_app(self, app):
        """Initialize a :class:`~flask.Flask` application for use with
        this extension.
        """
        self._jobs = []

        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions['restpoints'] = self
        app.restpoints_instance = self
        app.add_url_rule('/ping', 'ping', ping)
        app.add_url_rule('/time', 'time', time)
        app.add_url_rule('/status', 'status', status(self._jobs))