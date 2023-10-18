def init_app(self, app):
        """Initialize application in Flask-RBAC.
        Adds (RBAC, app) to flask extensions.
        Adds hook to authenticate permission before request.

        :param app: Flask object
        """

        app.config.setdefault('RBAC_USE_WHITE', False)
        self.use_white = app.config['RBAC_USE_WHITE']

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['rbac'] = _RBACState(self, app)

        self.acl.allow(anonymous, 'GET', 'static')
        app.before_first_request(self._setup_acl)

        app.before_request(self._authenticate)