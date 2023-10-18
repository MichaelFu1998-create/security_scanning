def asset(self):
        """ Returns the asset as instance of :class:`.asset.Asset`
        """
        if not self["asset"]:
            self["asset"] = self.asset_class(
                self["symbol"], blockchain_instance=self.blockchain
            )
        return self["asset"]