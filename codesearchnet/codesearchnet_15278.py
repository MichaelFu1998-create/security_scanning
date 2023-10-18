def _add_admin(self, app, **kwargs):
        """Add a Flask Admin interface to an application.

        :param flask.Flask app: A Flask application
        :param kwargs: Keyword arguments are passed through to :class:`flask_admin.Admin`
        :rtype: flask_admin.Admin
        """
        from flask_admin import Admin
        from flask_admin.contrib.sqla import ModelView

        admin = Admin(app, **kwargs)

        for flask_admin_model in self.flask_admin_models:
            if isinstance(flask_admin_model, tuple):  # assume its a 2 tuple
                if len(flask_admin_model) != 2:
                    raise TypeError

                model, view = flask_admin_model
                admin.add_view(view(model, self.session))

            else:
                admin.add_view(ModelView(flask_admin_model, self.session))

        return admin