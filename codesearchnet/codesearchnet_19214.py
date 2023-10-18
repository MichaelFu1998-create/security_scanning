def init_config(self, app):
        """Initialize configuration.

        :param app: An instance of :class:`~flask.Flask`.
        """
        config_apps = ['APP_', 'RATELIMIT_']
        flask_talisman_debug_mode = ["'unsafe-inline'"]
        for k in dir(config):
            if any([k.startswith(prefix) for prefix in config_apps]):
                app.config.setdefault(k, getattr(config, k))

        if app.config['DEBUG']:
            app.config.setdefault('APP_DEFAULT_SECURE_HEADERS', {})
            headers = app.config['APP_DEFAULT_SECURE_HEADERS']
            # ensure `content_security_policy` is not set to {}
            if headers.get('content_security_policy') != {}:
                headers.setdefault('content_security_policy', {})
                csp = headers['content_security_policy']
                # ensure `default-src` is not set to []
                if csp.get('default-src') != []:
                    csp.setdefault('default-src', [])
                    # add default `content_security_policy` value when debug
                    csp['default-src'] += flask_talisman_debug_mode