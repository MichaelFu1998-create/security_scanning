def get_indirect_url_lock_list(self, url, principal=None):
        """Return a list of valid lockDicts, that protect <path> directly or indirectly.

        If a principal is given, only locks owned by this principal are returned.
        Side effect: expired locks for this path and all parents are purged.
        """
        url = normalize_lock_root(url)
        lockList = []
        u = url
        while u:
            ll = self.storage.get_lock_list(
                u, include_root=True, include_children=False, token_only=False
            )
            for l in ll:
                if u != url and l["depth"] != "infinity":
                    continue  # We only consider parents with Depth: infinity
                # TODO: handle shared locks in some way?
                #                if (l["scope"] == "shared" and lock_scope == "shared"
                #                   and principal != l["principal"]):
                # continue  # Only compatible with shared locks by other users
                if principal is None or principal == l["principal"]:
                    lockList.append(l)
            u = util.get_uri_parent(u)
        return lockList