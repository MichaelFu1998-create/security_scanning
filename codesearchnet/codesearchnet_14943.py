def get_feature_names(self):
        """Get feature names.

        Returns
        -------
        feature_names : list of strings
            Names of the features produced by transform.
        """
        if self.__head_less:
            raise AttributeError(f'{self.__class__.__name__} instance configured to head less mode')
        elif not self.__head_dict:
            raise NotFittedError(f'{self.__class__.__name__} instance is not fitted yet')
        return list(self.__head_dict.values())