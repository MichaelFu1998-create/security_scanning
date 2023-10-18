def collect_files(self):
        """
        Return collected files links

        :rtype: list[static_bundle.files.StaticFileResult]
        """
        self.files = []
        for bundle in self.bundles:
            bundle.init_build(self, self.builder)
            bundle_files = bundle.prepare()
            self.files.extend(bundle_files)
        return self