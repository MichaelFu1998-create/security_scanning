def get_minifier(self):
        """
        Asset minifier
        Uses default minifier in bundle if it's not defined

        :rtype: static_bundle.minifiers.DefaultMinifier|None
        """
        if self.minifier is None:
            if not self.has_bundles():
                raise Exception("Unable to get default minifier, no bundles in build group")
            minifier = self.get_first_bundle().get_default_minifier()
        else:
            minifier = self.minifier
        if minifier:
            minifier.init_asset(self)
        return minifier