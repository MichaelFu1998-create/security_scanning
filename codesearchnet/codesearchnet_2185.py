def get_savable_components(self):
        """
        Returns the list of all of the components this model consists of that can be individually saved and restored.
        For instance the network or distribution.

        Returns:
            List of util.SavableComponent
        """
        components = self.get_components()
        components = [components[name] for name in sorted(components)]
        return set(filter(lambda x: isinstance(x, util.SavableComponent), components))