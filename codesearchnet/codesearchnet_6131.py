def _get_realm_entry(self, realm, user_name=None):
        """Return the matching user_map entry (falling back to default '*' if any)."""
        realm_entry = self.user_map.get(realm)
        if realm_entry is None:
            realm_entry = self.user_map.get("*")
        if user_name is None or realm_entry is None:
            return realm_entry
        return realm_entry.get(user_name)