def init_app(self, app):
        """Flask application initialization.

        Initialize the UI endpoints.  Connect all signals if
        `DEPOSIT_REGISTER_SIGNALS` is ``True``.

        :param app: An instance of :class:`flask.Flask`.
        """
        self.init_config(app)
        app.register_blueprint(ui.create_blueprint(
            app.config['DEPOSIT_RECORDS_UI_ENDPOINTS']
        ))
        app.extensions['invenio-deposit'] = _DepositState(app)
        if app.config['DEPOSIT_REGISTER_SIGNALS']:
            post_action.connect(index_deposit_after_publish, sender=app,
                                weak=False)