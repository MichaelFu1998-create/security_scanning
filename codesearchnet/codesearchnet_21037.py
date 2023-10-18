def startup(self, app):
        """Register connection's middleware and prepare self database."""
        self.database.init_async(app.loop)
        if not self.cfg.connection_manual:
            app.middlewares.insert(0, self._middleware)