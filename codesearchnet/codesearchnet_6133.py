def require_authentication(self, realm, environ):
        """Return True if this realm requires authentication (grant anonymous access otherwise)."""
        realm_entry = self._get_realm_entry(realm)
        if realm_entry is None:
            _logger.error(
                'Missing configuration simple_dc.user_mapping["{}"] (or "*"): '
                "realm is not accessible!".format(realm)
            )
        return realm_entry is not True