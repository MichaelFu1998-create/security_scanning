def register(self, app, options, first_registration=False):
        """Called by :meth:`Flask.register_blueprint` to register a blueprint
        on the application. This can be overridden to customize the register
        behavior. Keyword arguments from
        :func:`~flask.Flask.register_blueprint` are directly forwarded to this
        method in the `options` dictionary.
        """
        self.jsonrpc_site = options.get('jsonrpc_site')
        self._got_registered_once = True
        state = self.make_setup_state(app, options, first_registration)
        if self.has_static_folder and \
                not self.name + '.static' in state.app.view_functions.keys():
            state.add_url_rule(self.static_url_path + '/<path:filename>',
                               view_func=self.send_static_file,
                               endpoint='static')
        for deferred in self.deferred_functions:
            deferred(state)