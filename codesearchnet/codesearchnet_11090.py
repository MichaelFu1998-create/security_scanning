def get_effect(self, label: str) -> Effect:
        """
        Get an effect instance by label

        Args:
            label (str): The label for the effect instance

        Returns:
            Effect class instance
        """
        return self._get_resource(label, self._effects, "effect")