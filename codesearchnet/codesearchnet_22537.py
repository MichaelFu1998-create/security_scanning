def add_bundle(self, *args):
        """
        Add some bundle to build group

        :type bundle: static_bundle.bundles.AbstractBundle
        @rtype: BuildGroup
        """
        for bundle in args:
            if not self.multitype and self.has_bundles():
                first_bundle = self.get_first_bundle()
                if first_bundle.get_type() != bundle.get_type():
                    raise Exception(
                        'Different bundle types for one Asset: %s[%s -> %s]'
                        'check types or set multitype parameter to True'
                        % (self.name, first_bundle.get_type(), bundle.get_type())
                    )
            self.bundles.append(bundle)
        return self