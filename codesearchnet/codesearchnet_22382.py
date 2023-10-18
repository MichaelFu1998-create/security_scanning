def init_build(self, asset, builder):
        """
        Called when builder group collect files
        Resolves absolute url if relative passed

        :type asset: static_bundle.builders.Asset
        :type builder: static_bundle.builders.StandardBuilder
        """
        if not self.abs_path:
            rel_path = utils.prepare_path(self.rel_bundle_path)
            self.abs_bundle_path = utils.prepare_path([builder.config.input_dir, rel_path])
            self.abs_path = True
        self.input_dir = builder.config.input_dir