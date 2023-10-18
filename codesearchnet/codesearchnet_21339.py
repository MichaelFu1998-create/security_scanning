def r_assets(self, filetype, asset):
        """ Route for specific assets.

        :param filetype: Asset Type
        :param asset: Filename of an asset
        :return: Response
        """
        if filetype in self.assets and asset in self.assets[filetype] and self.assets[filetype][asset]:
            return send_from_directory(
                directory=self.assets[filetype][asset],
                filename=asset
            )
        abort(404)