def authenticate(self, token_value):
        """Check that the password is valid.

        This allows for revoking of a user's preview rights by changing the
        valid passwords.
        """
        try:
            backend_path, user_id = token_value.split(':', 1)
        except (ValueError, AttributeError):
            return False
        backend = auth.load_backend(backend_path)
        return bool(backend.get_user(user_id))