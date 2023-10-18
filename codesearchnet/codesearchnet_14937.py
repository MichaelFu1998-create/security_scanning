def get_feature_names(self):
        """Get feature names.

        Returns
        -------
        feature_names : list of strings
            Names of the features produced by transform.
        """
        return ['temperature', 'pressure'] + [f'solvent.{x}' for x in range(1, self.max_solvents + 1)] + \
               [f'solvent_amount.{x}' for x in range(1, self.max_solvents + 1)]