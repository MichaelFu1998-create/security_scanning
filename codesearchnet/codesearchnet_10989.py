def add_attribute(self, attr_type, name, components):
        """
        Add metadata about the mesh
        :param attr_type: POSITION, NORMAL etc
        :param name: The attribute name used in the program
        :param components: Number of floats
        """
        self.attributes[attr_type] = {"name": name, "components": components}