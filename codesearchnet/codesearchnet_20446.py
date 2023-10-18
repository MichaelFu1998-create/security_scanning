def require_accessibility(self, user, method):
        """Ensure we are allowed to access this resource."""
        if method == 'OPTIONS':
            # Authorization should not be checked on an OPTIONS request.
            return

        authz = self.meta.authorization
        if not authz.is_accessible(user, method, self):
            # User is not authorized; raise an appropriate message.
            authz.unaccessible()