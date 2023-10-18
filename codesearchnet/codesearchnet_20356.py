def assert_operations(self, *args):
        """Assets if the requested operations are allowed in this context."""
        if not set(args).issubset(self.allowed_operations):
            raise http.exceptions.Forbidden()