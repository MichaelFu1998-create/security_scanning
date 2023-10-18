def init_app(self, app):
        """Flask application initialization.

        Initialize the REST endpoints.  Connect all signals if
        `DEPOSIT_REGISTER_SIGNALS` is True.

        :param app: An instance of :class:`flask.Flask`.
        """
        self.init_config(app)
        blueprint = rest.create_blueprint(
            app.config['DEPOSIT_REST_ENDPOINTS']
        )

        # FIXME: This is a temporary fix. This means that
        # invenio-records-rest's endpoint_prefixes cannot be used before
        # the first request or in other processes, ex: Celery tasks.
        @app.before_first_request
        def extend_default_endpoint_prefixes():
            """Extend redirects between PID types."""
            endpoint_prefixes = utils.build_default_endpoint_prefixes(
                dict(app.config['DEPOSIT_REST_ENDPOINTS'])
            )
            current_records_rest = app.extensions['invenio-records-rest']
            overlap = set(endpoint_prefixes.keys()) & set(
                current_records_rest.default_endpoint_prefixes
            )
            if overlap:
                raise RuntimeError(
                    'Deposit wants to override endpoint prefixes {0}.'.format(
                        ', '.join(overlap)
                    )
                )
            current_records_rest.default_endpoint_prefixes.update(
                endpoint_prefixes
            )

        app.register_blueprint(blueprint)
        app.extensions['invenio-deposit-rest'] = _DepositState(app)
        if app.config['DEPOSIT_REGISTER_SIGNALS']:
            post_action.connect(index_deposit_after_publish, sender=app,
                                weak=False)