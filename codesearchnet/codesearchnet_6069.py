def resolve_provider(self, path):
        """Get the registered DAVProvider for a given path.

        Returns:
            tuple: (share, provider)
        """
        # Find DAV provider that matches the share
        share = None
        lower_path = path.lower()
        for r in self.sorted_share_list:
            # @@: Case sensitivity should be an option of some sort here;
            # os.path.normpath might give the preferred case for a filename.
            if r == "/":
                share = r
                break
            elif lower_path == r or lower_path.startswith(r + "/"):
                share = r
                break

        if share is None:
            return None, None
        return share, self.provider_map.get(share)