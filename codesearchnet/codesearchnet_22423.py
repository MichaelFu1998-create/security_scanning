def init_app(self, app):
        """Setup before_request, after_request handlers for tracing.
        """
        app.config.setdefault("TRACY_REQUIRE_CLIENT", False)
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions['restpoints'] = self
        app.before_request(self._before)
        app.after_request(self._after)