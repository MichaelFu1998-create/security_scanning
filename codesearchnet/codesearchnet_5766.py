def credentials(self):
        """The credentials for the current user or None if unavailable."""
        ctx = _app_ctx_stack.top

        if not hasattr(ctx, _CREDENTIALS_KEY):
            ctx.google_oauth2_credentials = self.storage.get()

        return ctx.google_oauth2_credentials