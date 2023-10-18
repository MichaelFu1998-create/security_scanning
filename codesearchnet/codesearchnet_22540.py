def create_asset(self, name, **kwargs):
        """
        Create asset

        :type name: unicode|str
        :rtype: Asset
        """
        asset = Asset(self, name, **kwargs)
        self.assets[name] = asset
        return asset