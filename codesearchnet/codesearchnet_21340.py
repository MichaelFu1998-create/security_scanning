def register_assets(self):
        """ Merge and register assets, both as routes and dictionary

        :return: None
        """
        self.blueprint.add_url_rule(
            # Register another path to ensure assets compatibility
            "{0}.secondary/<filetype>/<asset>".format(self.static_url_path),
            view_func=self.r_assets,
            endpoint="secondary_assets",
            methods=["GET"]
        )