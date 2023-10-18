def get_flask_admin_app(self, url: Optional[str] = None, secret_key: Optional[str] = None):
        """Create a Flask application.

        :param url: Optional mount point of the admin application. Defaults to ``'/'``.
        :rtype: flask.Flask
        """
        from flask import Flask

        app = Flask(__name__)

        if secret_key:
            app.secret_key = secret_key

        self._add_admin(app, url=(url or '/'))
        return app