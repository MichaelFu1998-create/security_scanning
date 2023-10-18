def get_path(self, scope: Scope) -> str:
        """
        Given the ASGI scope, return the `path` string to serve up,
        with OS specific path seperators, and any '..', '.' components removed.
        """
        return os.path.normpath(os.path.join(*scope["path"].split("/")))