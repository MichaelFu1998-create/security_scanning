def _get_user_class(self, name):
        """Get or create a user class of the given type."""
        self._user_classes.setdefault(name, _make_user_class(self, name))
        return self._user_classes[name]