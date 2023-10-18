def collect_links(self, env=None):
        """
        Return links without build files
        """
        for asset in self.assets.values():
            if asset.has_bundles():
                asset.collect_files()
        if env is None:
            env = self.config.env
        if env == static_bundle.ENV_PRODUCTION:
            self._minify(emulate=True)
        self._add_url_prefix()