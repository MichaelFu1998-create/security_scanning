def create_entity(self, name, gl_structure, description=None):
        """
        Create an entity and add it to the model.

        :param name: The entity name.
        :param gl_structure: The entity's general ledger structure.
        :param description: The entity description.

        :returns: The created entity.
        """

        new_entity = Entity(name, gl_structure, description=description)
        self.entities.append(new_entity)
        return new_entity