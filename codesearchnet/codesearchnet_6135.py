def digest_auth_user(self, realm, user_name, environ):
        """Computes digest hash A1 part."""
        user = self._get_realm_entry(realm, user_name)
        if user is None:
            return False
        password = user.get("password")
        environ["wsgidav.auth.roles"] = user.get("roles", [])
        return self._compute_http_digest_a1(realm, user_name, password)