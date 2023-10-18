def refresh(self):
        """ Refresh the data from the API server
        """
        asset = self.blockchain.rpc.get_asset(self.identifier)
        if not asset:
            raise AssetDoesNotExistsException(self.identifier)
        super(Asset, self).__init__(asset, blockchain_instance=self.blockchain)
        if self.full:
            if "bitasset_data_id" in asset:
                self["bitasset_data"] = self.blockchain.rpc.get_object(
                    asset["bitasset_data_id"]
                )
            self["dynamic_asset_data"] = self.blockchain.rpc.get_object(
                asset["dynamic_asset_data_id"]
            )