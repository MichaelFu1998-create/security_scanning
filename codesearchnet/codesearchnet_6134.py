def basic_auth_user(self, realm, user_name, password, environ):
        """Returns True if this user_name/password pair is valid for the realm,
        False otherwise. Used for basic authentication."""
        user = self._get_realm_entry(realm, user_name)

        if user is not None and password == user.get("password"):
            environ["wsgidav.auth.roles"] = user.get("roles", [])
            return True
        return False