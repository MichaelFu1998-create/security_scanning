def context(self):
        """Provides an admin context for workers."""
        if not self._context:
            self._context = context.get_admin_context()
        return self._context