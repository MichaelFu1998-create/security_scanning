def create_component(self, name, description=None):
        """
        Create a sub component in the business component.

        :param name: The new component's name.
        :param description: The new component's description.

        :returns: The created component.
        """

        new_comp = Component(name, self.gl, description=description)
        new_comp.set_parent_path(self.path)
        self.components.append(new_comp)
        return new_comp