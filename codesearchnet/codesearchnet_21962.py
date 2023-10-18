def setting_values(self, skip=None):
        """
        Returns dict of all setting values (removes the helpstrings).
        """
        if not skip:
            skip = []

        return dict(
                (k, v[1])
                for k, v in six.iteritems(self._instance_settings)
                if not k in skip)