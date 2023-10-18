def remove_component(self, name):
        """
        Remove a sub component from the component.

        :param name: The name of the component to remove.
        """

        component_to_remove = None
        for c in self.components:
            if c.name == name:
                component_to_remove = c
        if component_to_remove is not None:
            self.components.remove(component_to_remove)