def get_component(self, component_name):
        """
        Looks up a component by its name.

        Args:
            component_name: The name of the component to look up.
        Returns:
            The component for the provided name or None if there is no such component.
        """
        mapping = self.get_components()
        return mapping[component_name] if component_name in mapping else None