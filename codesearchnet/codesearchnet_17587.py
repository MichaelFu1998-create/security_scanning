def remove_entity(self, name):
        """
        Remove an entity from the model.

        :param name: The name of the entity to remove.
        """

        entity_to_remove = None
        for e in self.entities:
            if e.name == name:
                entity_to_remove = e
        if entity_to_remove is not None:
            self.entities.remove(entity_to_remove)