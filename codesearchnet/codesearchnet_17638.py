def get_component(self, name):
        """
        Retrieve a child component given its name.

        :param name: The name of the component.

        :returns: The component.
        """

        return [c for c in self.components if c.name == name][0]