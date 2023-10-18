def ref_url_to_path(self, ref_url):
        """Convert a refUrl to a path, by stripping the share prefix.

        Used to calculate the <path> from a storage key by inverting get_ref_url().
        """
        return "/" + compat.unquote(util.lstripstr(ref_url, self.share_path)).lstrip(
            "/"
        )