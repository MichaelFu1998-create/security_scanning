def make_build(self):
        """
        Move files / make static build
        """
        for asset in self.assets.values():
            if asset.has_bundles():
                asset.collect_files()
        if not os.path.exists(self.config.output_dir):
            os.makedirs(self.config.output_dir)
        if self.config.copy_only_bundles:
            for asset in self.assets.values():
                if not asset.minify and asset.files:
                    for f in asset.files:
                        copy_file(f.abs_path, self._get_output_path(f.abs_path))
        else:
            copy_excludes = {}
            for asset in self.assets.values():
                if asset.minify and asset.files:
                    for f in asset.files:
                        copy_excludes[f.abs_path] = f
            for root, dirs, files in os.walk(self.config.input_dir):
                for fpath in files:
                    current_file_path = os.path.join(root, fpath)
                    if current_file_path not in copy_excludes:
                        copy_file(current_file_path, self._get_output_path(current_file_path))
        self._minify()