def set_features(self, features):
        """Set features in the disco#info object.

        All existing features are removed from `self`.

        :Parameters:
            - `features`: list of features.
        :Types:
            - `features`: sequence of `unicode`
        """
        for var in self.features:
            self.remove_feature(var)

        for var in features:
            self.add_feature(var)